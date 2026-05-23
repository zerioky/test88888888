"""
user_model.py — V18
=====================
Leia apprend qui est l'utilisateur au fil des échanges.

Sans LLM. Analyse statistique des messages reçus.

Ce module répond à : "à qui est-ce que je parle ?"
Leia adapte sa densité conceptuelle, son niveau de certitude,
sa longueur de réponse, son registre — depuis des données réelles.

Ce n'est pas de la personnalisation superficielle :
c'est une vraie modélisation de l'interlocuteur
construite à partir des signaux linguistiques objectifs.
"""

from __future__ import annotations
import re, json, os, time, math
from collections import Counter, deque
from typing import Any, Dict, List, Optional

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
}

# Mots philosophiques / conceptuels → indique un profil intellectuel élevé
_PHILOSOPHICAL_MARKERS = {
    "conscience","ontologie","phénoménologie","dialectique","épistémologie",
    "métaphysique","immanence","transcendance","contingence","nécessité",
    "intentionnalité","intersubjectivité","dasein","être","néant","liberté",
    "déterminisme","causalité","substance","essence","existence","temporalité",
    "durée","mémoire","perception","représentation","concept","catégorie",
    "jugement","raison","entendement","intuition","esthétique","éthique",
    "morale","valeur","norme","devoir","vertu","bonheur","finitude","mort",
}

# Marqueurs affectifs explicites
_AFFECTIVE_MARKERS = {
    "ressens","éprouve","souffre","aime","déteste","peur","angoisse",
    "joie","tristesse","colère","mélancolie","nostalgie","espoir","désir",
    "manque","besoin","touche","bouleverse","émeut","étonne","fascine",
}

# Styles de questions
_QUESTION_STYLES = {
    "socratique":   {"n'est-ce pas","mais alors","si","et si","donc si","cela implique"},
    "direct":       {"qu'est-ce que","comment","pourquoi","quand","qui","où","combien"},
    "rhétorique":   {"n'est-ce pas","tu vois","tu comprends","pas vrai","quand même"},
    "exploratoire": {"peut-être","je me demande","je ne sais pas","je cherche","j'hésite"},
}

# Domaines thématiques
_DOMAIN_KEYWORDS = {
    "philosophie":   {"conscience","être","temps","mémoire","liberté","existence",
                      "mort","sens","vérité","raison","valeur","bonheur"},
    "littérature":   {"roman","personnage","auteur","écriture","poème","style",
                      "narration","récit","fiction","langue","mot"},
    "sciences":      {"cerveau","neurone","évolution","physique","chimie","biologie",
                      "expérience","hypothèse","théorie","preuve","données"},
    "psychologie":   {"traumatisme","émotion","inconscient","pulsion","désir",
                      "relation","attachement","anxiété","identité","soi"},
    "art":           {"beauté","esthétique","musique","peinture","sculpture","forme",
                      "couleur","harmonie","création","expressivité"},
    "histoire":      {"guerre","révolution","société","politique","pouvoir","classe",
                      "progrès","déclin","époque","siècle","civilisation"},
}


class UserModel:
    """
    Modèle adaptatif de l'utilisateur.

    Apprend depuis les messages réels :
    - Niveau lexical
    - Domaines préférés
    - Style de questionnement
    - Tonalité émotionnelle
    - Longueur typique des messages
    - Rapport établi avec Leia

    Expose un signal que le core injecte dans le payload du weaver :
    → Leia adapte sa sortie à qui elle parle réellement.
    """

    def __init__(self, storage_path: str = "data/user_model_default.json"):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(storage_path) if os.path.dirname(storage_path) else ".", exist_ok=True)

        # Métriques de base
        self.message_count:        int   = 0
        self.total_words:          int   = 0
        self.total_unique_words:   int   = 0
        self.word_lengths:         List[float] = []

        # Profil lexical
        self.vocab_seen:           Counter = Counter()
        self.philosophical_hits:   int   = 0
        self.affective_hits:       int   = 0

        # Domaines
        self.domain_scores:        Dict[str,float] = {d: 0.0 for d in _DOMAIN_KEYWORDS}

        # Style de question
        self.question_style_scores: Dict[str,float] = {s: 0.0 for s in _QUESTION_STYLES}

        # Tonalité émotionnelle (sliding window)
        self._affect_window:       deque = deque(maxlen=20)

        # Longueurs récentes
        self._length_window:       deque = deque(maxlen=20)

        # Rapport
        self.rapport_score:        float = 0.3  # 0=froid, 1=profond
        self.challenge_count:      int   = 0   # fois où l'utilisateur conteste
        self.question_count:       int   = 0   # total de questions posées
        self.personal_count:       int   = 0   # confidences personnelles

        # Préférences
        self.preferred_length:     str   = "medium"  # short/medium/long
        self.vocab_level:          float = 0.5       # 0=simple, 1=très riche
        self.dominant_domain:      str   = ""
        self.question_style:       str   = "direct"

        # Historique léger
        self._history:             deque = deque(maxlen=30)
        self._load()

    # ── Persistance ───────────────────────────────────────────────────────────
    def _load(self):
        if not os.path.exists(self.storage_path): return
        try:
            with open(self.storage_path, encoding="utf-8") as f:
                data = json.load(f)
            self.message_count      = int(data.get("message_count", 0))
            self.total_words        = int(data.get("total_words", 0))
            self.philosophical_hits = int(data.get("philosophical_hits", 0))
            self.affective_hits     = int(data.get("affective_hits", 0))
            self.domain_scores      = data.get("domain_scores", self.domain_scores)
            self.question_style_scores = data.get("question_style_scores", self.question_style_scores)
            self.rapport_score      = float(data.get("rapport_score", 0.3))
            self.challenge_count    = int(data.get("challenge_count", 0))
            self.question_count     = int(data.get("question_count", 0))
            self.personal_count     = int(data.get("personal_count", 0))
            self.vocab_level        = float(data.get("vocab_level", 0.5))
            self.dominant_domain    = data.get("dominant_domain", "")
            self.question_style     = data.get("question_style", "direct")
            self.preferred_length   = data.get("preferred_length", "medium")
            self.vocab_seen         = Counter(data.get("vocab_seen", {}))
            for h in data.get("history", []):
                self._history.append(h)
            for v in data.get("affect_window", []):
                self._affect_window.append(v)
            for v in data.get("length_window", []):
                self._length_window.append(v)
        except Exception:
            pass

    def _save(self):
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump({
                    "message_count":      self.message_count,
                    "total_words":        self.total_words,
                    "philosophical_hits": self.philosophical_hits,
                    "affective_hits":     self.affective_hits,
                    "domain_scores":      {k: round(v,4) for k,v in self.domain_scores.items()},
                    "question_style_scores": {k: round(v,4) for k,v in self.question_style_scores.items()},
                    "rapport_score":      round(self.rapport_score, 4),
                    "challenge_count":    self.challenge_count,
                    "question_count":     self.question_count,
                    "personal_count":     self.personal_count,
                    "vocab_level":        round(self.vocab_level, 4),
                    "dominant_domain":    self.dominant_domain,
                    "question_style":     self.question_style,
                    "preferred_length":   self.preferred_length,
                    "vocab_seen":         dict(self.vocab_seen.most_common(300)),
                    "history":            list(self._history)[-20:],
                    "affect_window":      list(self._affect_window),
                    "length_window":      list(self._length_window),
                    "timestamp":          _now(),
                }, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # ── Apprentissage depuis un message ──────────────────────────────────────
    def observe(self, message: str, utterance_parsed: Optional[Dict[str,Any]] = None) -> None:
        """
        Observe un message utilisateur et met à jour le modèle.
        utterance_parsed : résultat de UserUtteranceParser.signal() (optionnel)
        """
        if not message: return
        low = message.lower()
        words = re.findall(r"[\wÀ-ÿ']{2,}", low)
        content = [w for w in words if w not in _STOP and len(w) > 3]

        self.message_count += 1
        self.total_words   += len(words)
        self._length_window.append(len(words))

        # Vocabulaire
        self.vocab_seen.update(content)

        # Niveau lexical : proportion de mots longs (>7 car) et philosophiques
        long_words = sum(1 for w in content if len(w) > 7)
        phi_words  = sum(1 for w in content if w in _PHILOSOPHICAL_MARKERS)
        aff_words  = sum(1 for w in content if w in _AFFECTIVE_MARKERS)
        self.philosophical_hits += phi_words
        self.affective_hits     += aff_words

        # Mise à jour vocab_level (EMA)
        if content:
            richness = _clamp((long_words + phi_words * 2) / len(content))
            self.vocab_level = _clamp(self.vocab_level * 0.92 + richness * 0.08)

        # Domaines
        for domain, keywords in _DOMAIN_KEYWORDS.items():
            hits = sum(1 for w in content if w in keywords)
            if hits:
                self.domain_scores[domain] = _clamp(
                    self.domain_scores[domain] * 0.9 + hits * 0.02)
        self.dominant_domain = max(self.domain_scores, key=self.domain_scores.get)

        # Style de question
        if "?" in message:
            self.question_count += 1
            for style, markers in _QUESTION_STYLES.items():
                hits = sum(1 for m in markers if m in low)
                if hits:
                    self.question_style_scores[style] = _clamp(
                        self.question_style_scores[style] * 0.9 + hits * 0.05)
            self.question_style = max(self.question_style_scores,
                                      key=self.question_style_scores.get)

        # Confidences personnelles
        if any(m in low for m in {"je ressens","j'éprouve","j'ai peur",
                                   "je souffre","ça me touche","je me sens"}):
            self.personal_count += 1
            self.rapport_score = _clamp(self.rapport_score + 0.015)

        # Challenges / contestations
        if any(m in low for m in {"pas d'accord","faux","tu as tort","erreur",
                                   "je ne suis pas","non mais","au contraire"}):
            self.challenge_count += 1
            # Les challenges intellectuels renforcent légèrement le rapport
            self.rapport_score = _clamp(self.rapport_score + 0.005)

        # Décroissance naturelle du rapport si longs silences
        # (non gérée ici, serait dans tick_inner_life)

        # Longueur préférée
        avg_len = (sum(self._length_window) / len(self._length_window)
                   if self._length_window else 10)
        if avg_len < 8:
            self.preferred_length = "short"
        elif avg_len > 25:
            self.preferred_length = "long"
        else:
            self.preferred_length = "medium"

        # Tonalité affective
        affect = 0.0
        if utterance_parsed:
            stance = utterance_parsed.get("stance","neutre")
            affect_map = {"certitude": 0.6, "doute": -0.2,
                          "scepticisme": -0.1, "neutre": 0.0,
                          "nuance_négative": -0.3}
            affect = affect_map.get(stance, 0.0)
        self._affect_window.append(affect)

        # Historique
        self._history.append({
            "wc":      len(words),
            "phi":     phi_words,
            "aff":     aff_words,
            "is_q":    "?" in message,
            "ts":      _now(),
        })

        if self.message_count % 3 == 0:
            self._save()

    # ── Profil courant ────────────────────────────────────────────────────────
    def profile(self) -> Dict[str, Any]:
        """Retourne le profil complet de l'utilisateur."""
        avg_affect = (sum(self._affect_window) / len(self._affect_window)
                      if self._affect_window else 0.0)
        avg_len = (sum(self._length_window) / len(self._length_window)
                   if self._length_window else 10)

        # Top mots : les plus utilisés hors stop
        top_words = [w for w, _ in self.vocab_seen.most_common(20)
                     if w not in _STOP and len(w) > 4]

        # Top domaines
        top_domains = sorted(self.domain_scores.items(),
                              key=lambda x: x[1], reverse=True)[:3]

        return {
            "message_count":     self.message_count,
            "vocab_level":       round(self.vocab_level, 3),
            "vocab_richness":    "élevée" if self.vocab_level > 0.6 else
                                 "moyenne" if self.vocab_level > 0.35 else "simple",
            "dominant_domain":   self.dominant_domain,
            "top_domains":       [d for d,_ in top_domains],
            "question_style":    self.question_style,
            "preferred_length":  self.preferred_length,
            "avg_message_words": round(avg_len, 1),
            "rapport_score":     round(self.rapport_score, 3),
            "rapport_label":     "profond" if self.rapport_score > 0.7 else
                                 "établi" if self.rapport_score > 0.45 else
                                 "naissant" if self.rapport_score > 0.25 else "froid",
            "avg_affect":        round(avg_affect, 3),
            "emotional_tone":    "positif" if avg_affect > 0.15 else
                                 "négatif" if avg_affect < -0.15 else "neutre",
            "philosophical_hits": self.philosophical_hits,
            "affective_hits":    self.affective_hits,
            "challenge_count":   self.challenge_count,
            "question_count":    self.question_count,
            "personal_count":    self.personal_count,
            "top_words":         top_words[:10],
        }

    # ── Recommandations d'adaptation ─────────────────────────────────────────
    def adaptation_hints(self) -> Dict[str, Any]:
        """
        Ce que Leia devrait adapter dans sa réponse pour cet utilisateur.
        Injecté dans le payload du weaver comme contrainte douce.
        """
        prof = self.profile()
        hints: Dict[str, Any] = {}

        # Longueur cible
        target_words = {"short": 8, "medium": 14, "long": 22}
        hints["target_length_words"] = target_words[prof["preferred_length"]]

        # Densité conceptuelle
        if prof["vocab_level"] > 0.6:
            hints["concept_density"] = "high"    # mots rares OK
            hints["abstraction_level"] = "high"
        elif prof["vocab_level"] > 0.35:
            hints["concept_density"] = "medium"
            hints["abstraction_level"] = "medium"
        else:
            hints["concept_density"] = "low"     # mots simples
            hints["abstraction_level"] = "low"

        # Niveau de certitude (si l'utilisateur aime le doute → douter plus)
        if prof["question_style"] == "exploratoire":
            hints["certainty_level"] = "low"
        elif prof["question_style"] == "direct":
            hints["certainty_level"] = "medium"
        else:
            hints["certainty_level"] = "medium"

        # Rapport → chaleur de la réponse
        hints["warmth"] = min(1.0, prof["rapport_score"] * 1.3)

        # Si l'utilisateur est philosophique → Leia peut être plus dense
        if prof["philosophical_hits"] > 5:
            hints["philosophical_depth"] = True

        # Si l'utilisateur est affectif → Leia répond plus avec l'affect
        if prof["affective_hits"] > 3 or prof["personal_count"] > 2:
            hints["affective_priority"] = True

        # Si contestations fréquentes → Leia peut nuancer davantage
        if prof["challenge_count"] > 3:
            hints["include_nuance"] = True

        return hints

    # ── Signal pour le core ───────────────────────────────────────────────────
    def signal(self, user_input: str = "") -> Dict[str, Any]:
        """Interface standard."""
        if self.message_count == 0:
            return {"available": False}

        prof  = self.profile()
        hints = self.adaptation_hints()

        return {
            "available":        True,
            "message_count":    prof["message_count"],
            "vocab_level":      prof["vocab_level"],
            "vocab_richness":   prof["vocab_richness"],
            "dominant_domain":  prof["dominant_domain"],
            "question_style":   prof["question_style"],
            "preferred_length": prof["preferred_length"],
            "rapport_score":    prof["rapport_score"],
            "rapport_label":    prof["rapport_label"],
            "emotional_tone":   prof["emotional_tone"],
            "top_words":        prof["top_words"][:6],
            "adaptation":       hints,
            "is_philosophical": prof["philosophical_hits"] > 5,
            "is_affective":     prof["affective_hits"] > 3,
        }

    def snapshot(self) -> Dict[str, Any]:
        return {
            "messages": self.message_count,
            "rapport":  round(self.rapport_score, 3),
            "domain":   self.dominant_domain,
            "level":    round(self.vocab_level, 3),
        }