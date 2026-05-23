# reading_living_consolidation_engine.py
# Project Leia / project_leia — V18
#
# Rôle:
#   Transformer une lecture en continuité mentale active : digestion progressive,
#   réflexion interne, consolidation durable et initiative cognitive.
#   Ce module ne contient aucune réponse publique prête à dire. Il ne stocke que
#   des concepts, pressions, questions, relations, effets internes
#   et maintenant : la structure argumentative des textes lus.
#
# Nouveau V18 : ArgumentStructureExtractor
#   Détecter dans le texte les marqueurs linguistiques de thèse, objection,
#   concession et conclusion — sans dépendance externe.
#   Résultat : des atomes de structure logique que Leia peut porter
#   pour distinguer ce qu'un auteur affirme de ce qu'il réfute.

from __future__ import annotations

import json
import math
import re
import time
from collections import Counter, deque
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Deque, Dict, Iterable, List, Mapping, Optional, Tuple

_WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9_'-]+", re.UNICODE)
_STOP = {
    "avec", "dans", "pour", "sans", "vers", "entre", "comme", "mais", "donc", "ainsi",
    "elle", "elles", "nous", "vous", "leur", "leurs", "cette", "celui", "celle", "ceux",
    "être", "etre", "avoir", "fait", "faire", "plus", "tout", "tous", "toute", "très", "tres",
    "cela", "ceci", "dont", "quand", "quoi", "comment", "pourquoi", "parce", "encore",
    "page", "fragment", "livre", "pdf", "texte", "passage", "lecture",
}
_GENERIC = {
    "trace", "presence", "présence", "continuité", "continuite", "doute", "question", "prudence",
    "appui", "lien", "liens", "mouvement", "rythme", "résonance", "resonance", "curiosité", "curiosite",
}


def _clamp(value: Any, lo: float = 0.0, hi: float = 1.0) -> float:
    try:
        f = float(value)
    except Exception:
        return lo
    if math.isnan(f) or math.isinf(f):
        return lo
    return max(lo, min(hi, f))


def _short(text: Any, limit: int = 80) -> str:
    s = re.sub(r"\s+", " ", str(text or "").strip().lower())
    s = s.strip(" .,:;!?—[]{}()\"'")
    if len(s) > limit:
        s = s[:limit].rsplit(" ", 1)[0] or s[:limit]
    return s


def _words(text: Any) -> List[str]:
    out: List[str] = []
    for w in _WORD_RE.findall(str(text or "").lower()):
        w = w.strip("'_- ")
        if len(w) < 3 or w in _STOP or w in _GENERIC:
            continue
        out.append(w)
    return out


def _unique(items: Iterable[Any], limit: int = 20) -> List[str]:
    out: List[str] = []
    seen = set()
    for item in items or []:
        if isinstance(item, Mapping):
            cands = [item.get(k) for k in ("label", "concept", "keyword", "source", "target", "axis")]
            if isinstance(item.get("between"), (list, tuple)):
                cands += list(item.get("between")[:2])
            if isinstance(item.get("keywords"), list):
                cands += item.get("keywords")[:8]
        elif isinstance(item, (list, tuple, set)):
            cands = list(item)
        else:
            cands = [item]
        for cand in cands:
            t = _short(cand)
            if not t or len(t) < 3 or t in seen or t in _GENERIC:
                continue
            if re.match(r"^(relier|clarifier|explorer|résoudre|resoudre|ouvrir_question)\b", t):
                continue
            seen.add(t)
            out.append(t)
            if len(out) >= limit:
                return out
    return out


@dataclass
class ArgumentNode:
    """Un nœud argumentatif V19 — rôle + voix + liens + coréférence."""
    role: str
    fragment: str
    concept: str
    strength: float
    voice: str = "unknown"
    links: List[Dict[str, Any]] = field(default_factory=list)
    resolved_concept: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ─────────────────────────────────────────────────────────────────
# VoiceTracker — de qui est la voix dans cette phrase ?
# ─────────────────────────────────────────────────────────────────

_REPORTED_PATTERNS = [
    re.compile(r"\b(certains?\s+(pensent?|disent?|soutiennent?|croient?|affirment?|prétendent?))\b", re.I | re.U),
    re.compile(r"\b(d['\']aucuns?\s+(pensent?|disent?|soutiennent?|croient?))\b", re.I | re.U),
    re.compile(r"\b(beaucoup\s+(pensent?|croient?|soutiennent?))\b", re.I | re.U),
    re.compile(r"\b(on\s+(a\s+)?(longtemps\s+)?(prétend|croit|cru|dit|soutient|pense)\s*(que|souvent)?)\b", re.I | re.U),
    re.compile(r"\b(l['\']idée\s+reçue|la\s+doxa|le\s+sens\s+commun|l['\']opinion\s+courante)\b", re.I | re.U),
    re.compile(r"\b(il\s+est\s+(souvent|généralement)\s+(dit|admis|pensé|cru))\b", re.I | re.U),
    re.compile(r"\b(la\s+thèse\s+(adverse|opposée|contraire)|l['\']adversaire)\b", re.I | re.U),
]

_ATTRIBUTED_PATTERNS = [
    re.compile(r"\b(selon\s+[A-ZÀ-Ö][a-zà-ÿ]+)\b", re.U),
    re.compile(r"\b(d['\']après\s+[A-ZÀ-Ö][a-zà-ÿ]+)\b", re.U),
    re.compile(r"\b(pour\s+[A-ZÀ-Ö][a-zà-ÿ]+,)\b", re.U),
    re.compile(r"\b([A-ZÀ-Ö][a-zà-ÿ]+\s+(affirme|soutient|pense|croit|écrit|dit)\s+que)\b", re.U),
]

_OWN_VOICE_PATTERNS = [
    re.compile(r"\b(je\s+soutiens|je\s+défends|je\s+pense|je\s+crois|ma\s+thèse|notre\s+position)\b", re.I | re.U),
    re.compile(r"\b(l['\']auteur\s+(affirme|soutient|défend|conclut|démontre))\b", re.I | re.U),
    re.compile(r"\b(on\s+peut\s+(donc|ainsi)\s+(conclure|affirmer|soutenir))\b", re.I | re.U),
    re.compile(r"\b(nous\s+(défendons|soutenons|affirmons|concluons))\b", re.I | re.U),
]


def _detect_voice(sentence: str) -> str:
    s = sentence
    s_lower = s.lower()
    for pat in _REPORTED_PATTERNS:
        if pat.search(s_lower):
            return "reported"
    for pat in _ATTRIBUTED_PATTERNS:
        if pat.search(s):
            return "attributed"
    for pat in _OWN_VOICE_PATTERNS:
        if pat.search(s_lower):
            return "own"
    return "unknown"


# ─────────────────────────────────────────────────────────────────
# CoreferenceResolver — suivre un concept à travers les phrases
# ─────────────────────────────────────────────────────────────────

_REFERENCE_SHELLS = {
    "réalité", "phénomène", "chose", "idée", "concept", "notion", "fait",
    "cela", "ceci", "celui", "celle", "ceux", "celles", "celui-ci", "celle-ci",
    "processus", "mécanisme", "principe", "faculté", "propriété", "aspect",
}

_PRONOUN_SUBJECTS = {"il", "elle", "ils", "elles", "ce", "cela", "ceci", "celui", "celle"}


class CoreferenceResolver:
    """
    Résolution légère de coréférence entre phrases.
    Fenêtre glissante des derniers concepts nommés.
    Quand une phrase extrait un concept générique ou pronominal,
    on le remplace par le dernier concept spécifique connu.
    """

    def __init__(self, window: int = 4):
        self.window = window
        self._history: List[str] = []

    def reset(self) -> None:
        self._history = []

    def resolve(self, raw_concept: str, sentence: str) -> str:
        c = raw_concept.strip().lower()
        if c in _REFERENCE_SHELLS or c in _PRONOUN_SUBJECTS or len(c) < 4:
            extracted = self._extract_from_sentence(sentence)
            if extracted and extracted not in _REFERENCE_SHELLS:
                self._update(extracted)
                return extracted
            if self._history:
                return self._history[-1]
            return raw_concept
        self._update(c)
        return c

    def _update(self, concept: str) -> None:
        if not concept or len(concept) < 3:
            return
        if concept in self._history:
            self._history.remove(concept)
        self._history.append(concept)
        if len(self._history) > self.window:
            self._history.pop(0)

    def _extract_from_sentence(self, sentence: str) -> str:
        candidates = [
            w for w in re.findall(r"\b[a-zà-ÿ]{5,}\b", sentence.lower())
            if w not in _STOP and w not in _GENERIC and w not in _REFERENCE_SHELLS
        ]
        if not candidates:
            return ""
        candidates.sort(key=lambda w: -len(w))
        return candidates[0]

    def last_concept(self) -> str:
        return self._history[-1] if self._history else ""


# ─────────────────────────────────────────────────────────────────
# ArgumentChain — relier les nœuds par flux logique
# ─────────────────────────────────────────────────────────────────

_CHAIN_RULES: List[Tuple[str, str, str]] = [
    ("thèse",      "objection",   "opposes"),
    ("thèse",      "concession",  "qualifies"),
    ("thèse",      "conclusion",  "supports"),
    ("objection",  "concession",  "concedes"),
    ("objection",  "conclusion",  "rebounds"),
    ("concession", "conclusion",  "rebuts"),
    ("reported",   "objection",   "critiques"),
    ("attributed", "objection",   "disputes"),
]

_MIN_OVERLAP = 0.15


def _concept_overlap(a: str, b: str) -> float:
    wa = set(re.findall(r"[a-zà-ÿ]{4,}", a.lower()))
    wb = set(re.findall(r"[a-zà-ÿ]{4,}", b.lower()))
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / min(len(wa), len(wb))


def build_argument_chain(nodes: List[Any]) -> List[Dict[str, Any]]:
    """
    Relie les nœuds argumentatifs.
    1. Liens structurels entre rôles consécutifs.
    2. Liens lexicaux (recouvrement de concept) entre nœuds ≤ 4 d'écart.
    Modifie les nœuds in-place (nœuds doivent être des ArgumentNode).
    """
    chains: List[Dict[str, Any]] = []

    for i in range(len(nodes) - 1):
        a, b = nodes[i], nodes[i + 1]
        role_a = a.role if a.voice != "reported" else "reported"
        for from_r, to_r, ltype in _CHAIN_RULES:
            if role_a == from_r and b.role == to_r:
                ov = _concept_overlap(a.resolved_concept or a.concept,
                                      b.resolved_concept or b.concept)
                st = round(_clamp(0.5 + ov * 0.4), 3)
                a.links.append({"to_index": i + 1, "relation": ltype, "strength": st})
                chains.append({"from_index": i, "to_index": i + 1,
                                "relation": ltype, "strength": st})
                break

    for i in range(len(nodes)):
        for j in range(i + 2, min(i + 5, len(nodes))):
            a, b = nodes[i], nodes[j]
            ov = _concept_overlap(a.resolved_concept or a.concept,
                                  b.resolved_concept or b.concept)
            if ov >= _MIN_OVERLAP:
                if not any(lnk["to_index"] == j for lnk in a.links):
                    ltype = "echoes" if b.role == "conclusion" else "resonates"
                    st = round(_clamp(ov * 0.7), 3)
                    a.links.append({"to_index": j, "relation": ltype, "strength": st})
                    chains.append({"from_index": i, "to_index": j,
                                   "relation": ltype, "strength": st})

    return chains


# ─────────────────────────────────────────────────────────────────
# Marqueurs linguistiques par rôle — patterns compilés une seule fois
# ─────────────────────────────────────────────────────────────────

_ARG_PATTERNS: Dict[str, List[re.Pattern]] = {
    "thèse": [
        re.compile(r"\b(je\s+soutiens|je\s+défends|je\s+pense\s+que|je\s+crois\s+que)\b", re.I | re.U),
        re.compile(r"\b(l[''a]\s+thèse|l[''a]\s+idée\s+centrale|l[''a]\s+argument\s+principal)\b", re.I | re.U),
        re.compile(r"\b(il\s+s[''a]agit\s+de|l[''a]auteur\s+affirme|l[''a]auteur\s+soutient|l[''a]auteur\s+défend)\b", re.I | re.U),
        re.compile(r"\b(on\s+peut\s+affirmer|nous\s+affirmons|cela\s+signifie\s+que)\b", re.I | re.U),
        re.compile(r"\b(en\s+réalité|en\s+vérité|fondamentalement|essentiellement)\b", re.I | re.U),
    ],
    "objection": [
        re.compile(r"\b(cependant|néanmoins|toutefois|or\s+|en\s+revanche|à\s+l[''a]opposé)\b", re.I | re.U),
        re.compile(r"\b(certains\s+diront|on\s+objectera|on\s+pourrait\s+objecter|l[''a]objection)\b", re.I | re.U),
        re.compile(r"\b(mais\s+(il\s+faut|on\s+peut|cela\s+ne|ceci\s+ne))\b", re.I | re.U),
        re.compile(r"\b(contrairement\s+à|à\s+l[''a]encontre|s[''i]il\s+est\s+vrai\s+que)\b", re.I | re.U),
    ],
    "concession": [
        re.compile(r"\b(certes|il\s+est\s+vrai\s+que|on\s+reconnaît\s+que|admettons\s+que)\b", re.I | re.U),
        re.compile(r"\b(même\s+si|bien\s+que|quoique|sans\s+doute|peut[- ]être)\b", re.I | re.U),
        re.compile(r"\b(on\s+concède\s+que|il\s+faut\s+reconnaître)\b", re.I | re.U),
    ],
    "conclusion": [
        re.compile(r"\b(donc|ainsi|par\s+conséquent|il\s+s[''e]ensuit\s+que)\b", re.I | re.U),
        re.compile(r"\b(en\s+définitive|en\s+conclusion|finalement|c[''e]est\s+pourquoi)\b", re.I | re.U),
        re.compile(r"\b(on\s+peut\s+conclure|nous\s+pouvons\s+affirmer|il\s+résulte\s+que)\b", re.I | re.U),
        re.compile(r"\b(en\s+somme|en\s+bref|pour\s+conclure|tout\s+cela\s+montre)\b", re.I | re.U),
    ],
}

# Mots de liaison qui seuls ne suffisent pas (trop courts, trop fréquents)
_WEAK_SOLO = {"or", "mais", "donc", "certes"}


class ArgumentStructureExtractor:
    """
    Extrait la structure argumentative d'un texte philosophique ou théorique.

    Ne produit pas d'interprétation — seulement des nœuds structurés :
    quel fragment joue quel rôle logique, quel concept il porte.

    Fonctionne sans dépendance externe. Repose sur des heuristiques
    linguistiques françaises et sur l'extraction du concept dominant
    par sélection du nom le plus dense de la phrase.
    """

    def __init__(self):
        self._coref = CoreferenceResolver(window=5)

    def extract(self, text: str, max_nodes: int = 20) -> List[Dict[str, Any]]:
        """
        V19 — extraction complète :
        1. Détection de rôle (thèse/objection/concession/conclusion)
        2. Détection de voix (own/reported/attributed)
        3. Résolution de coréférence (concept suivi entre phrases)
        4. Chaînage argumentatif (liens logiques entre nœuds)
        """
        if not text or len(text.strip()) < 60:
            return []

        nodes = self._build_nodes(text, max_nodes)
        if not nodes:
            return []

        # Chaîner les nœuds — modifie les nœuds in-place
        chains = build_argument_chain(nodes)

        dicts = [n.to_dict() for n in nodes]
        # Ajouter les chaînes dans les dicts
        for i, d in enumerate(dicts):
            d["links"] = nodes[i].links

        return dicts

    def _build_nodes(self, text: str, max_nodes: int = 20) -> List["ArgumentNode"]:
        """Méthode interne partagée : construit la liste de nœuds depuis un texte."""
        if not text or len(text.strip()) < 60:
            return []
        self._coref.reset()
        sentences = self._split_sentences(text)
        nodes: List[ArgumentNode] = []
        seen_concepts: set = set()
        for sent in sentences:
            if len(sent.strip()) < 12:
                continue
            role, strength = self._classify(sent)
            voice = _detect_voice(sent)
            if not role:
                if voice == "reported":
                    role, strength = "thèse", 0.45
                elif voice == "attributed":
                    role, strength = "thèse", 0.40
                else:
                    continue
            raw = self._extract_concept(sent)
            resolved = self._coref.resolve(raw, sent)
            key = resolved or raw
            if not key or key in seen_concepts:
                continue
            seen_concepts.add(key)
            nodes.append(ArgumentNode(
                role=role, fragment=_short(sent, 80), concept=raw,
                strength=round(strength, 3), voice=voice,
                links=[], resolved_concept=resolved,
            ))
            if len(nodes) >= max_nodes:
                break
        return nodes

    def extract_with_chains(self, text: str, max_nodes: int = 20) -> Dict[str, Any]:
        """Retourne nodes + chains + métadonnées pour interbook detection."""
        nodes = self._build_nodes(text, max_nodes)
        if not nodes:
            return {"nodes": [], "chains": [], "summary": self.summarize([]),
                    "own_theses": [], "reported_positions": []}
        chains = build_argument_chain(nodes)
        return {
            "nodes": [n.to_dict() for n in nodes],
            "chains": chains,
            "summary": self.summarize([n.to_dict() for n in nodes]),
            "own_theses": [n.resolved_concept or n.concept for n in nodes
                           if n.role == "thèse" and n.voice in ("own", "unknown", "attributed")],
            "reported_positions": [n.resolved_concept or n.concept for n in nodes
                                    if n.voice == "reported"],
        }

    def _split_sentences(self, text: str) -> List[str]:
        """Découpe le texte en phrases sur ponctuation forte."""
        raw = re.split(r"(?<=[.!?;])\s+", text)
        out = []
        for s in raw:
            s = s.strip()
            if len(s) > 15:
                out.append(s)
        return out[:200]   # limite pour éviter les textes énormes

    def _classify(self, sentence: str) -> Tuple[Optional[str], float]:
        """
        Retourne (rôle, force) si un marqueur est détecté.
        Retourne (None, 0) sinon.
        """
        s_lower = sentence.lower()
        for role, patterns in _ARG_PATTERNS.items():
            for pat in patterns:
                m = pat.search(s_lower)
                if m:
                    matched = m.group(0).strip()
                    if matched in _WEAK_SOLO and len(s_lower.split()) < 5:
                        continue
                    # Force proportionnelle à la longueur de la phrase (plus c'est développé, plus c'est fort)
                    strength = _clamp(0.3 + min(0.5, len(sentence.split()) / 40.0))
                    return role, strength
        return None, 0.0

    # Connecteurs qui ne doivent jamais être le concept dominant d'une phrase
    _CONNECTORS = {
        # Connecteurs logiques
        "cependant", "néanmoins", "toutefois", "pourtant", "certes",
        "donc", "ainsi", "finalement", "définitive", "conclusion",
        "revanche", "contraire", "encontre", "opposé", "même",
        "bien", "quoique", "admettons", "reconnaît", "reconnaître",
        "soutiens", "défends", "soutient", "affirme", "conclure",
        "résulte", "ensuit", "conséquent", "pourquoi",
        # Sujets de discours rapporté — pas des concepts
        "certains", "aucuns", "beaucoup", "partisans", "opposants",
        "adversaire", "adversaires", "plupart", "plusieurs",
        # Verbes modaux de discours
        "pensent", "croient", "prétendent", "soutiennent", "affirment",
        "disent", "conçoivent", "imaginent", "supposent",
    }

    def _extract_concept(self, sentence: str) -> str:
        """
        Extrait le concept dominant d'une phrase.
        Exclut les connecteurs logiques et les verbes de discours.
        Préfère les noms spécifiques (longs, non-connecteurs).
        """
        candidates = [
            w for w in re.findall(r"\b[a-zà-ÿ]{4,}\b", sentence.lower())
            if (w not in _STOP and w not in _GENERIC
                and w not in self._CONNECTORS
                and not w.endswith("ment"))   # éviter les adverbes
        ]
        if not candidates:
            return ""
        # Trier par longueur décroissante, préférer les substantifs
        candidates.sort(key=lambda w: -len(w))
        return candidates[0] if candidates else ""

    def summarize(self, nodes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Résumé de structure : combien de thèses, objections, conclusions.
        Utile pour savoir si un texte est fortement argumentatif ou descriptif.
        """
        counts: Dict[str, int] = {}
        for n in nodes:
            role = n.get("role", "")
            counts[role] = counts.get(role, 0) + 1
        return {
            "node_count": len(nodes),
            "by_role": counts,
            "is_argumentative": counts.get("thèse", 0) > 0 and (
                counts.get("objection", 0) > 0 or counts.get("conclusion", 0) > 0
            ),
        }


# Instance globale du extracteur — pas de state, réutilisable
_arg_extractor = ArgumentStructureExtractor()


@dataclass
class ReadingReflection:
    source: str
    created_at: float
    active_concepts: List[str] = field(default_factory=list)
    relation_focus: List[Dict[str, Any]] = field(default_factory=list)
    unresolved_questions: List[str] = field(default_factory=list)
    contradictions: List[Dict[str, Any]] = field(default_factory=list)
    transformations: List[Dict[str, Any]] = field(default_factory=list)
    consolidation_targets: Dict[str, float] = field(default_factory=dict)
    initiative_seed: Dict[str, Any] = field(default_factory=dict)
    argument_structure: List[Dict[str, Any]] = field(default_factory=list)   # V18
    argument_summary: Dict[str, Any] = field(default_factory=dict)            # V18
    own_theses: List[str] = field(default_factory=list)                        # V19
    reported_positions: List[str] = field(default_factory=list)               # V19
    argument_chains: List[Dict[str, Any]] = field(default_factory=list)        # V19
    metrics: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class ReadingLivingConsolidationEngine:
    """Mémoire active de lecture.

    Le moteur fait quatre choses :
    1. extraire les concepts vivants d'un modèle de livre;
    2. produire une réflexion interne non conversationnelle;
    3. renforcer les concepts avec le temps et les échanges;
    4. signaler quand une initiative cognitive devient légitime.
    """

    def __init__(self, storage_path: str = "data/reading_living_consolidation.json", max_history: int = 32) -> None:
        self.storage_path = Path(storage_path)
        self.max_history = max(4, int(max_history or 32))
        self.reflections: Deque[Dict[str, Any]] = deque(maxlen=self.max_history)
        self.consolidated_concepts: Dict[str, float] = {}
        self.open_questions: Deque[Dict[str, Any]] = deque(maxlen=64)
        self.reactivation_history: Deque[Dict[str, Any]] = deque(maxlen=96)
        self.last_initiative_at: float = 0.0
        self.last_consolidation_at: float = time.time()
        self.load_state()

    def load_state(self) -> None:
        try:
            if self.storage_path.exists():
                data = json.loads(self.storage_path.read_text(encoding="utf-8"))
                self.reflections = deque(data.get("reflections", [])[-self.max_history:], maxlen=self.max_history)
                self.consolidated_concepts = {str(k): _clamp(v) for k, v in data.get("consolidated_concepts", {}).items()}
                self.open_questions = deque(data.get("open_questions", [])[-64:], maxlen=64)
                self.reactivation_history = deque(data.get("reactivation_history", [])[-96:], maxlen=96)
                self.last_initiative_at = float(data.get("last_initiative_at", 0.0) or 0.0)
                self.last_consolidation_at = float(data.get("last_consolidation_at", time.time()) or time.time())
        except Exception:
            pass

    def save_state(self) -> None:
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "reflections": list(self.reflections),
                "consolidated_concepts": self.consolidated_concepts,
                "open_questions": list(self.open_questions),
                "reactivation_history": list(self.reactivation_history),
                "last_initiative_at": self.last_initiative_at,
                "last_consolidation_at": self.last_consolidation_at,
            }
            tmp = self.storage_path.with_suffix(self.storage_path.suffix + ".tmp")
            tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            tmp.replace(self.storage_path)
        except Exception:
            pass

    def reflect_on_book(self, book_model: Mapping[str, Any], pdf_result: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
        if not isinstance(book_model, Mapping) or not book_model:
            return {"available": False, "reason": "empty_book_model"}
        pdf_result = pdf_result or {}
        source = str(book_model.get("source") or pdf_result.get("file") or "book")
        axes = _unique(book_model.get("axes", []), 18)
        keywords = _unique(book_model.get("keywords", []), 22)
        tensions = list(book_model.get("tensions", []) or [])[:18]
        relations_raw = list(book_model.get("relations", []) or [])[:24]
        questions = _unique(book_model.get("question_axes", []), 14)
        transformations_raw = list(book_model.get("transformations", []) or [])[:18]
        pressures = book_model.get("concept_pressures", {}) if isinstance(book_model.get("concept_pressures", {}), Mapping) else {}

        concepts = []
        scored = []
        for c in axes + keywords:
            score = _clamp(pressures.get(c, 0.45))
            if c not in concepts:
                concepts.append(c)
                scored.append((score, c))
        scored.sort(reverse=True)
        active_concepts = [c for _, c in scored[:18]] or concepts[:18]

        relation_focus: List[Dict[str, Any]] = []
        for rel in relations_raw:
            if not isinstance(rel, Mapping):
                continue
            src = _short(rel.get("source") or rel.get("from"))
            tgt = _short(rel.get("target") or rel.get("to"))
            if not src or not tgt or src == tgt:
                continue
            weight = _clamp(rel.get("weight", max(pressures.get(src, 0.0), pressures.get(tgt, 0.0), 0.35)))
            relation_focus.append({"source": src, "target": tgt, "type": _short(rel.get("type") or rel.get("relation") or "lié", 28), "pressure": round(weight, 4)})

        contradictions: List[Dict[str, Any]] = []
        for t in tensions:
            if not isinstance(t, Mapping):
                continue
            between = t.get("between") if isinstance(t.get("between"), (list, tuple)) else []
            if len(between) >= 2:
                pressure = _clamp(t.get("pressure", 0.45))
                contradictions.append({
                    "between": [_short(between[0]), _short(between[1])],
                    "relation": _short(t.get("relation") or "tension", 28),
                    "pressure": round(pressure, 4),
                    "unresolved": bool(t.get("unresolved", pressure > 0.5)),
                })

        transformations: List[Dict[str, Any]] = []
        for tr in transformations_raw:
            if isinstance(tr, Mapping):
                axis = _short(tr.get("axis") or tr.get("concept"))
                if axis:
                    transformations.append({
                        "axis": axis,
                        "novelty": round(_clamp(tr.get("novelty", 0.45)), 4),
                        "integration_pressure": round(_clamp(tr.get("integration_pressure", pressures.get(axis, 0.42))), 4),
                    })

        targets: Dict[str, float] = {}
        for idx, c in enumerate(active_concepts[:24]):
            targets[c] = max(targets.get(c, 0.0), _clamp(0.70 - idx * 0.018 + pressures.get(c, 0.0) * 0.25))
        for rel in relation_focus[:16]:
            targets[rel["source"]] = max(targets.get(rel["source"], 0.0), _clamp(rel.get("pressure", 0.0) * 0.92))
            targets[rel["target"]] = max(targets.get(rel["target"], 0.0), _clamp(rel.get("pressure", 0.0) * 0.86))
        for tr in transformations:
            targets[tr["axis"]] = max(targets.get(tr["axis"], 0.0), _clamp(tr.get("integration_pressure", 0.0)))

        for concept, value in targets.items():
            self.consolidated_concepts[concept] = _clamp(self.consolidated_concepts.get(concept, 0.0) * 0.82 + value * 0.28)
        for q in questions[:12]:
            self.open_questions.appendleft({"question_axis": q, "pressure": round(targets.get(q, 0.48), 4), "source": source, "created_at": time.time(), "answered": False})

        # V18 — Extraction de la structure argumentative
        # On cherche le texte brut dans pdf_result ou book_model
        raw_text = ""
        if isinstance(pdf_result, Mapping):
            raw_text = str(pdf_result.get("text", pdf_result.get("content", pdf_result.get("raw_text", ""))))
        if not raw_text and isinstance(book_model, Mapping):
            raw_text = str(book_model.get("raw_text", book_model.get("text", book_model.get("content", ""))))
        # Fallback : concaténer les valeurs textuelles du book_model si texte court
        if len(raw_text) < 200 and isinstance(book_model, Mapping):
            parts = []
            for v in book_model.values():
                if isinstance(v, str) and len(v) > 20:
                    parts.append(v)
                elif isinstance(v, list):
                    for item in v:
                        if isinstance(item, str) and len(item) > 20:
                            parts.append(item)
            raw_text = raw_text + " " + " ".join(parts[:30])

        arg_result = _arg_extractor.extract_with_chains(raw_text, max_nodes=20)
        arg_nodes = arg_result["nodes"]
        arg_summary = arg_result["summary"]
        # Thèses propres et positions rapportées — utiles pour inter_book_tension
        _own_theses = arg_result.get("own_theses", [])
        _reported_positions = arg_result.get("reported_positions", [])

        # Les concepts de la structure argumentative renforcent les consolidation_targets
        for node in arg_nodes:
            concept = node.get("concept", "")
            if concept and len(concept) > 3:
                strength = float(node.get("strength", 0.4))
                # Les thèses et conclusions comptent plus que les concessions
                role_weight = {"thèse": 1.0, "conclusion": 0.9, "objection": 0.8, "concession": 0.6}.get(
                    node.get("role", ""), 0.5
                )
                targets[concept] = max(targets.get(concept, 0.0), _clamp(strength * role_weight * 0.7))

        initiative_seed = self._build_initiative_seed(active_concepts, questions, contradictions, transformations)
        reflection = ReadingReflection(
            source=source,
            created_at=time.time(),
            active_concepts=active_concepts[:18],
            relation_focus=relation_focus[:16],
            unresolved_questions=questions[:12],
            contradictions=contradictions[:12],
            transformations=transformations[:12],
            consolidation_targets={k: round(v, 4) for k, v in sorted(targets.items(), key=lambda kv: -kv[1])[:32]},
            initiative_seed=initiative_seed,
            argument_structure=arg_nodes[:20],
            argument_summary=arg_summary,
            own_theses=_own_theses[:12],
            reported_positions=_reported_positions[:8],
            argument_chains=arg_result.get("chains", [])[:24],
            metrics={
                "concept_count": len(active_concepts),
                "relation_count": len(relation_focus),
                "question_count": len(questions),
                "contradiction_count": len(contradictions),
                "transformation_count": len(transformations),
                "argument_node_count": len(arg_nodes),
                "is_argumentative": arg_summary.get("is_argumentative", False),
                "pages_read": pdf_result.get("pages_read", pdf_result.get("pages", 0)) if isinstance(pdf_result, Mapping) else 0,
            },
        ).to_dict()
        self.reflections.appendleft(reflection)
        self.last_consolidation_at = time.time()
        self.save_state()
        return reflection

    def _build_initiative_seed(self, concepts: List[str], questions: List[str], contradictions: List[Mapping[str, Any]], transformations: List[Mapping[str, Any]]) -> Dict[str, Any]:
        top = concepts[:6]
        unresolved = questions[:4]
        pressure = _clamp(len(top) / 8.0 * 0.24 + len(unresolved) / 6.0 * 0.30 + len(contradictions) / 8.0 * 0.28 + len(transformations) / 8.0 * 0.18)
        return {
            "active": bool(top or unresolved),
            "pressure": round(pressure, 4),
            "concepts": top,
            "questions": unresolved,
            "reason": "unresolved_reading_pressure" if unresolved or contradictions else "recent_reading_continuity",
        }

    def reactivate(self, query_text: str = "", limit: int = 12) -> Dict[str, Any]:
        qwords = set(_words(query_text))
        scored: List[Tuple[float, str]] = []
        for concept, pressure in self.consolidated_concepts.items():
            cwords = set(_words(concept))
            overlap = len(qwords & cwords) / max(1, len(cwords)) if qwords else 0.0
            recency = 0.0
            for idx, ref in enumerate(list(self.reflections)[:8]):
                if concept in ref.get("active_concepts", []) or concept in ref.get("consolidation_targets", {}):
                    recency = max(recency, 0.16 / (idx + 1))
            scored.append((_clamp(pressure * 0.70 + overlap * 0.22 + recency), concept))
        scored.sort(reverse=True)
        active = [c for _, c in scored[:max(1, int(limit or 12))]]
        open_q = list(self.open_questions)[:10]
        out = {
            "available": bool(active or self.reflections),
            "active_concepts": active,
            "concept_pressures": {c: round(dict((name, score) for score, name in scored).get(c, 0.0), 4) for c in active},
            "open_questions": open_q,
            "last_reflection": self.reflections[0] if self.reflections else {},
            "initiative": self.initiative_probe(query_text=query_text),
        }
        self.reactivation_history.appendleft({"query": _short(query_text, 120), "active": active[:8], "at": time.time()})
        self.save_state()
        return out

    def consolidate_idle(self, elapsed: float = 1.0) -> Dict[str, Any]:
        elapsed = max(0.1, float(elapsed or 1.0))
        decay = 0.997 ** min(300.0, elapsed)
        for k in list(self.consolidated_concepts.keys()):
            self.consolidated_concepts[k] = _clamp(self.consolidated_concepts[k] * decay)
            if self.consolidated_concepts[k] < 0.035:
                del self.consolidated_concepts[k]
        # Les questions ouvertes gagnent un peu de pression quand elles restent non résolues.
        for q in list(self.open_questions)[:24]:
            if not q.get("answered"):
                q["pressure"] = round(_clamp(q.get("pressure", 0.3) + 0.004 * min(10.0, elapsed)), 4)
        self.last_consolidation_at = time.time()
        self.save_state()
        return {"available": True, "concept_count": len(self.consolidated_concepts), "open_questions": len(self.open_questions), "initiative": self.initiative_probe()}

    def absorb_dialogue_effect(self, user_input: str, response: str, context: Mapping[str, Any], after_effect: Mapping[str, Any]) -> Dict[str, Any]:
        text = f"{user_input} {response}"
        words = set(_words(text))
        reinforced: Dict[str, float] = {}
        for concept in list(self.consolidated_concepts.keys()):
            cwords = set(_words(concept))
            if words & cwords:
                gain = _clamp(0.025 + len(words & cwords) / max(1, len(cwords)) * 0.055)
                self.consolidated_concepts[concept] = _clamp(self.consolidated_concepts.get(concept, 0.0) + gain)
                reinforced[concept] = round(gain, 4)
        for q in list(self.open_questions):
            qwords = set(_words(q.get("question_axis", "")))
            if words & qwords and len(response.split()) > 5:
                q["pressure"] = round(_clamp(q.get("pressure", 0.3) * 0.88), 4)
        self.save_state()
        return {"available": True, "reinforced": reinforced, "initiative": self.initiative_probe(query_text=user_input)}

    def initiative_probe(self, query_text: str = "") -> Dict[str, Any]:
        now = time.time()
        cooldown = max(0.0, 90.0 - (now - self.last_initiative_at))
        top = sorted(self.consolidated_concepts.items(), key=lambda kv: -kv[1])[:8]
        questions = [q for q in list(self.open_questions)[:12] if not q.get("answered")]
        pressure = _clamp(
            (top[0][1] if top else 0.0) * 0.42
            + (sum(float(q.get("pressure", 0.0)) for q in questions[:4]) / max(1, min(4, len(questions)))) * 0.36
            + min(1.0, len(self.reflections) / 6.0) * 0.12
            + (0.10 if query_text and any(w in query_text.lower() for w in ("livre", "pdf", "bergson", "mémoire", "memoire")) else 0.0)
        )
        allowed = pressure >= 0.46 and cooldown <= 0.0
        return {
            "available": bool(top or questions),
            "should_surface": bool(allowed),
            "pressure": round(pressure, 4),
            "cooldown": round(cooldown, 2),
            "concepts": [c for c, _ in top[:5]],
            "questions": [q.get("question_axis") for q in questions[:4]],
            "reason": "reading_continuity_pressure" if allowed else "held_silently",
        }

    def mark_initiative_used(self) -> None:
        self.last_initiative_at = time.time()
        self.save_state()

    def snapshot(self) -> Dict[str, Any]:
        return {
            "reflections": list(self.reflections)[:6],
            "consolidated_concepts": {k: round(v, 4) for k, v in sorted(self.consolidated_concepts.items(), key=lambda kv: -kv[1])[:32]},
            "open_questions": list(self.open_questions)[:10],
            "initiative": self.initiative_probe(),
        }
