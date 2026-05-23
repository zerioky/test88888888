"""
user_utterance_parser.py — V18
================================
Compréhension réelle de ce que dit l'utilisateur.

Sans LLM. Utilise spaCy fr_core_news_lg si disponible,
sinon repli sur analyse morphosyntaxique légère.

Ce module répond à : "qu'a-t-il voulu dire ?"
Pas seulement les mots — la structure, l'intention, la posture.

Installe : pip install spacy && python -m spacy download fr_core_news_lg
"""

from __future__ import annotations
import re, json, os, time, math
from typing import Any, Dict, List, Optional, Tuple
from collections import Counter

# ── Tentative d'import spaCy ──────────────────────────────────────────────────
try:
    import spacy
    _SPACY_AVAILABLE = True
except ImportError:
    spacy = None  # type: ignore
    _SPACY_AVAILABLE = False

_NLP = None  # modèle chargé paresseusement

def _get_nlp():
    global _NLP
    if _NLP is not None:
        return _NLP
    if not _SPACY_AVAILABLE:
        return None
    for model in ("fr_core_news_lg", "fr_core_news_md", "fr_core_news_sm"):
        try:
            _NLP = spacy.load(model)
            return _NLP
        except Exception:
            continue
    return None

# ── Patterns d'intention ──────────────────────────────────────────────────────
_QUESTION_MARKS      = {"?", "est-ce", "qu'est-ce", "qu'est", "quel", "quelle",
                         "quels", "quelles", "comment", "pourquoi", "combien",
                         "lequel", "laquelle", "lesquels"}
_DOUBT_MARKERS       = {"peut-être", "je ne sais", "j'hésite", "vraiment",
                         "tu crois", "tu penses vraiment", "doute", "incertain",
                         "incertaine", "je doute", "bizarre", "étrange"}
_CHALLENGE_MARKERS   = {"non", "faux", "tort", "erreur", "je ne suis pas",
                         "pas d'accord", "contredis", "conteste", "mais tu",
                         "pourtant", "cependant", "en réalité", "au contraire"}
_CONFIDENCE_MARKERS  = {"sûr", "certain", "certaine", "clairement", "évidemment",
                         "bien sûr", "absolument", "forcément", "nécessairement"}
_PERSONAL_MARKERS    = {"je ressens", "j'éprouve", "j'ai peur", "je souffre",
                         "j'aime", "je hais", "ça me touche", "ça me fait",
                         "je me sens", "mon", "ma", "mes"}
_RHETORICAL          = {"n'est-ce pas", "non ?", "tu vois", "pas vrai",
                         "tu comprends", "n'est pas", "quand même"}

# Stopwords français compacts
_STOP = {
    "le","la","les","un","une","des","de","du","et","en","est","à","au","aux",
    "il","elle","ils","elles","on","je","tu","nous","vous","se","sa","son",
    "ses","me","te","lui","leur","leurs","que","qui","quoi","dont","où",
    "mais","ou","donc","or","ni","car","si","lors","alors","ainsi",
    "très","plus","moins","bien","tout","même","aussi","encore","toujours",
    "jamais","rien","ne","pas","plus","déjà","avec","sans","sous","sur",
    "dans","par","pour","vers","chez","comme","quand","comment","combien",
    "ce","cet","cette","ces","mon","ton","son","ma","ta","notre","votre",
    "être","avoir","faire","aller","voir","venir","dire","savoir","pouvoir",
    "vouloir","falloir","prendre","donner","trouver","penser","croire",
    "sembler","paraître"
}

# ── Fonctions utilitaires ─────────────────────────────────────────────────────
def _clamp(v, lo=0.0, hi=1.0):
    try: return max(lo, min(hi, float(v)))
    except: return lo

def _tokens(text: str) -> List[str]:
    return re.findall(r"[\wÀ-ÿ']+", text.lower())

def _content_words(text: str) -> List[str]:
    return [t for t in _tokens(text) if t not in _STOP and len(t) > 2]


# ── Analyseur léger (sans spaCy) ──────────────────────────────────────────────
class _LightParser:
    """
    Analyse morphosyntaxique légère par règles.
    Utilisée quand spaCy n'est pas disponible.
    Moins précis, mais fonctionnel.
    """

    _COPULAS = {"est","sont","étaient","était","serait","sera","suis","es"}
    _QUESTION_STARTERS = {
        "est-ce que","est-ce qu","qu'est-ce que","qu'est-ce qu",
        "pourquoi","comment","quand","où","qui","que","quoi","quel","quelle",
        "combien","lequel","laquelle"
    }

    def parse(self, text: str) -> Dict[str, Any]:
        raw = text.strip()
        low = raw.lower()
        toks = _tokens(raw)
        content = _content_words(raw)

        # Intent
        intent = self._detect_intent(low, toks)
        stance = self._detect_stance(low)
        focus  = self._detect_focus(content)
        named  = []   # sans spaCy pas de NER fiable
        subject, verb_root, obj = self._light_svo(toks, low)

        return {
            "intent":       intent,
            "stance":       stance,
            "focus_concept": focus[0] if focus else "",
            "focus_concepts": focus[:4],
            "named_entities": named,
            "subject":      subject,
            "verb_root":    verb_root,
            "object":       obj,
            "is_question":  "?" in raw or intent.startswith("question"),
            "is_personal":  self._is_personal(low),
            "word_count":   len(toks),
            "content_words": content,
            "raw":          raw,
            "parser":       "light",
        }

    def _detect_intent(self, low: str, toks: List[str]) -> str:
        if any(m in low for m in _CHALLENGE_MARKERS):
            return "challenge"
        for qs in self._QUESTION_STARTERS:
            if low.startswith(qs) or f" {qs} " in low:
                return "question_directe"
        if "?" in low:
            if any(m in low for m in _RHETORICAL):
                return "question_rhétorique"
            if any(m in low for m in _DOUBT_MARKERS):
                return "question_avec_doute"
            return "question"
        if any(m in low for m in _PERSONAL_MARKERS):
            return "confidence_personnelle"
        if any(m in low for m in _DOUBT_MARKERS):
            return "expression_doute"
        return "affirmation"

    def _detect_stance(self, low: str) -> str:
        score = 0
        if any(m in low for m in _DOUBT_MARKERS):      score -= 2
        if any(m in low for m in _CHALLENGE_MARKERS):  score -= 1
        if any(m in low for m in _CONFIDENCE_MARKERS): score += 2
        if any(m in low for m in _PERSONAL_MARKERS):   score += 1
        if score >= 2:   return "certitude"
        if score <= -2:  return "doute"
        if score == -1:  return "scepticisme"
        return "neutre"

    def _detect_focus(self, content: List[str]) -> List[str]:
        # Les mots de contenu les plus longs = probablement conceptuels
        scored = sorted(set(content), key=lambda w: (len(w), content.count(w)), reverse=True)
        return scored[:6]

    def _light_svo(self, toks: List[str], low: str) -> Tuple[str, str, str]:
        # Heuristique grossière : pronom/nom + verbe + complément
        pronouns = {"je","tu","il","elle","on","nous","vous","ils","elles","leia"}
        subj = next((t for t in toks if t.lower() in pronouns), "")
        verbs = {"est","pense","croit","sait","voit","sent","aime","veut",
                 "trouve","dit","parle","comprend","ressent","doute"}
        vrb  = next((t for t in toks if t.lower() in verbs), "")
        # Objet : premier mot de contenu après le verbe
        if vrb and vrb in toks:
            idx = toks.index(vrb)
            rest = [t for t in toks[idx+1:] if t not in _STOP and len(t) > 2]
            obj = rest[0] if rest else ""
        else:
            obj = ""
        return subj, vrb, obj

    def _is_personal(self, low: str) -> bool:
        return bool(re.search(r"\b(je|mon|ma|mes|moi|j')\b", low))


# ── Analyseur spaCy (précis) ──────────────────────────────────────────────────
class _SpacyParser:
    """
    Analyse syntaxique complète avec spaCy.
    Extraction de dépendances, NER, lemmatisation.
    """

    _INTENT_VERBS = {
        "demander","questionner","savoir","comprendre","vouloir",
        "expliquer","dire","penser","croire","affirmer","nier",
        "contester","douter","ressentir","éprouver","confier"
    }

    def parse(self, text: str, nlp) -> Dict[str, Any]:
        doc = nlp(text)
        intent   = self._detect_intent(doc, text.lower())
        stance   = self._detect_stance(doc, text.lower())
        focus    = self._extract_focus(doc)
        named    = self._named_entities(doc)
        subj, verb_root, obj = self._extract_svo(doc)
        propositions = self._extract_propositions(doc)
        modifiers    = self._extract_modifiers(doc)
        content      = [t.lemma_.lower() for t in doc
                        if not t.is_stop and not t.is_punct
                        and len(t.text) > 2 and t.is_alpha]

        return {
            "intent":         intent,
            "stance":         stance,
            "focus_concept":  focus[0] if focus else "",
            "focus_concepts": focus[:6],
            "named_entities": named,
            "subject":        subj,
            "verb_root":      verb_root,
            "object":         obj,
            "propositions":   propositions,
            "modifiers":      modifiers,
            "is_question":    "?" in text or intent.startswith("question"),
            "is_personal":    any(t.lower_ in {"je","mon","ma","mes","moi"} for t in doc),
            "is_negative":    any(t.dep_ == "neg" for t in doc),
            "word_count":     len([t for t in doc if not t.is_punct]),
            "content_words":  content,
            "raw":            text,
            "parser":         "spacy",
        }

    def _detect_intent(self, doc, low: str) -> str:
        if any(m in low for m in _CHALLENGE_MARKERS):
            return "challenge"
        # Interrogation directe via POS TAG
        if any(t.tag_ in ("PUNCT",) and t.text == "?" for t in doc):
            if any(t.lemma_ in {"pourquoi","comment","combien"} for t in doc):
                return "question_philosophique"
            if any(m in low for m in _RHETORICAL):
                return "question_rhétorique"
            return "question"
        if any(m in low for m in _PERSONAL_MARKERS):
            return "confidence_personnelle"
        if any(m in low for m in _DOUBT_MARKERS):
            return "expression_doute"
        # Vérifier si ROOT est un verbe d'opinion
        for t in doc:
            if t.dep_ == "ROOT" and t.lemma_ in self._INTENT_VERBS:
                return "affirmation_opinion"
        return "affirmation"

    def _detect_stance(self, doc, low: str) -> str:
        neg = sum(1 for t in doc if t.dep_ == "neg")
        doubt = sum(1 for m in _DOUBT_MARKERS if m in low)
        cert  = sum(1 for m in _CONFIDENCE_MARKERS if m in low)
        score = cert * 2 - doubt * 2 - neg
        if score >= 2:  return "certitude"
        if score <= -2: return "doute"
        if neg > 0:     return "nuance_négative"
        return "neutre"

    def _extract_focus(self, doc) -> List[str]:
        """Les noms/noms propres les plus saillants = concepts focaux."""
        candidates = []
        for chunk in doc.noun_chunks:
            head = chunk.root
            if head.is_stop or head.is_punct: continue
            if len(head.text) < 3: continue
            score = 1.0
            # Sujet ou objet → plus important
            if head.dep_ in ("nsubj","obj","iobj","nsubj:pass"): score += 1.5
            # Gouverné par verbe principal → important
            if head.head.dep_ == "ROOT": score += 0.5
            candidates.append((score, head.lemma_.lower()))
        # Noms propres hors chunks
        for t in doc:
            if t.ent_type_ and t.is_alpha and len(t.text) > 2:
                candidates.append((1.8, t.lemma_.lower()))
        candidates.sort(reverse=True)
        seen = set()
        result = []
        for _, lem in candidates:
            if lem not in seen and lem not in _STOP:
                seen.add(lem)
                result.append(lem)
        return result[:8]

    def _named_entities(self, doc) -> List[Dict[str, str]]:
        return [{"text": ent.text, "label": ent.label_}
                for ent in doc.ents if len(ent.text) > 1]

    def _extract_svo(self, doc) -> Tuple[str, str, str]:
        subj = ""
        vrb  = ""
        obj  = ""
        for t in doc:
            if t.dep_ == "ROOT" and t.pos_ == "VERB":
                vrb = t.lemma_.lower()
            if t.dep_ in ("nsubj","nsubj:pass") and not subj:
                subj = t.lemma_.lower()
            if t.dep_ in ("obj","dobj","iobj") and not obj:
                obj = t.lemma_.lower()
        return subj, vrb, obj

    def _extract_propositions(self, doc) -> List[Dict[str, str]]:
        """Extrait des triplets (sujet, relation, objet) de la phrase."""
        props = []
        for t in doc:
            if t.pos_ != "VERB": continue
            subj = next((c.lemma_.lower() for c in t.children
                         if c.dep_ in ("nsubj","nsubj:pass")), "")
            obj  = next((c.lemma_.lower() for c in t.children
                         if c.dep_ in ("obj","dobj","attr","xcomp")), "")
            neg  = any(c.dep_ == "neg" for c in t.children)
            if subj and obj:
                props.append({
                    "subject":  subj,
                    "relation": ("ne_" if neg else "") + t.lemma_.lower(),
                    "object":   obj,
                })
        return props[:8]

    def _extract_modifiers(self, doc) -> List[str]:
        """Adverbes et adjectifs qui nuancent = posture épistémique."""
        mods = []
        for t in doc:
            if t.pos_ in ("ADV","ADJ") and not t.is_stop and len(t.text) > 3:
                mods.append(t.lemma_.lower())
        return mods[:6]


# ── Classe principale ─────────────────────────────────────────────────────────
class UserUtteranceParser:
    """
    Point d'entrée public.
    Choisit automatiquement le meilleur parseur disponible.
    """

    def __init__(self, storage_path: str = "data/utterance_history_default.json"):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(storage_path) if os.path.dirname(storage_path) else ".", exist_ok=True)
        self._light   = _LightParser()
        self._spacy   = _SpacyParser()
        self._history: List[Dict[str, Any]] = []
        self._load()

    # ── Persistence ───────────────────────────────────────────────────────────
    def _load(self):
        if not os.path.exists(self.storage_path): return
        try:
            with open(self.storage_path, encoding="utf-8") as f:
                data = json.load(f)
            self._history = data.get("history", [])[-30:]
        except Exception:
            pass

    def _save(self):
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump({"history": self._history[-30:], "ts": time.time()},
                          f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # ── Analyse principale ────────────────────────────────────────────────────
    def parse(self, text: str) -> Dict[str, Any]:
        """
        Analyse un message utilisateur.
        Retourne un dictionnaire riche utilisable par le core.
        """
        if not text or not text.strip():
            return {"intent": "silence", "stance": "neutre", "focus_concept": "",
                    "focus_concepts": [], "named_entities": [],
                    "subject": "", "verb_root": "", "object": "",
                    "is_question": False, "is_personal": False,
                    "word_count": 0, "content_words": [], "raw": text,
                    "parser": "none"}

        nlp = _get_nlp()
        if nlp is not None:
            result = self._spacy.parse(text, nlp)
        else:
            result = self._light.parse(text)

        # Enrichissement contextuel depuis l'historique
        result["contextual_continuity"] = self._contextual_continuity(result)
        result["timestamp"] = time.time()

        self._history.append({k: result[k] for k in
            ("intent","stance","focus_concept","is_question","timestamp")})
        if len(self._history) > 30:
            self._history = self._history[-30:]
        self._save()
        return result

    def _contextual_continuity(self, current: Dict[str, Any]) -> Dict[str, Any]:
        """Compare avec les tours précédents pour détecter la continuité thématique."""
        if len(self._history) < 2:
            return {"topic_change": False, "consecutive_questions": 0}
        prev = self._history[-1]
        topic_change = (
            current.get("focus_concept","") != prev.get("focus_concept","")
            and bool(current.get("focus_concept",""))
        )
        q_streak = 0
        for h in reversed(self._history):
            if h.get("is_question"):
                q_streak += 1
            else:
                break
        return {
            "topic_change": topic_change,
            "consecutive_questions": q_streak,
            "previous_intent": prev.get("intent",""),
        }

    # ── Signal pour le core ───────────────────────────────────────────────────
    def signal(self, text: str = "") -> Dict[str, Any]:
        """
        Interface standard du core.
        Retourne {"available": True, ...} avec l'analyse complète.
        """
        if not text:
            return {"available": False}
        parsed = self.parse(text)
        return {
            "available":    True,
            "intent":       parsed.get("intent",""),
            "stance":       parsed.get("stance",""),
            "focus_concept": parsed.get("focus_concept",""),
            "focus_concepts": parsed.get("focus_concepts",[]),
            "named_entities": parsed.get("named_entities",[]),
            "propositions": parsed.get("propositions",[]),
            "subject":      parsed.get("subject",""),
            "verb_root":    parsed.get("verb_root",""),
            "object":       parsed.get("object",""),
            "is_question":  parsed.get("is_question", False),
            "is_personal":  parsed.get("is_personal", False),
            "is_negative":  parsed.get("is_negative", False),
            "word_count":   parsed.get("word_count", 0),
            "content_words": parsed.get("content_words",[]),
            "contextual":   parsed.get("contextual_continuity",{}),
            "modifiers":    parsed.get("modifiers",[]),
            "parser_used":  parsed.get("parser",""),
        }

    def is_why_question(self, text: str) -> bool:
        """Détecte si l'utilisateur demande à Leia de s'expliquer."""
        _WHY = {"pourquoi","d'où","comment tu arrives","qu'est-ce qui te fait",
                "explique","tu peux expliquer","tu penses ça"}
        low = text.lower()
        return any(m in low for m in _WHY)

    def is_self_question(self, text: str) -> bool:
        """Détecte si l'utilisateur parle de Leia elle-même."""
        _SELF = {"tu es","t'es","tu ressens","tu penses","toi leia","leia tu",
                 "ce que tu","comment tu vis","qu'est-ce que tu","tu sais que"}
        low = text.lower()
        return any(m in low for m in _SELF) or "leia" in low

    def summary(self) -> str:
        """Résumé lisible pour l'UI debug."""
        if not self._history:
            return "(aucun historique)"
        last = self._history[-1]
        return (f"dernier intent={last.get('intent','')} "
                f"stance={last.get('stance','')} "
                f"focus={last.get('focus_concept','')}")