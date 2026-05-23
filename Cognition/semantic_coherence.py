"""
semantic_coherence.py — V18
==============================
Mesure si Leia dit vraiment ce qu'elle veut dire.

Sans LLM, sans FastText (trop lourd à inclure).
Utilise une approche TF-IDF + cosine sur les concepts actifs.

Si numpy est disponible : vecteurs TF-IDF propres.
Sinon : Jaccard pondéré + overlap.

Ce module permet à Leia de savoir :
- Est-ce que ma réponse reflète vraiment mes concepts actifs ?
- Ai-je dérivé vers des mots de remplissage ?
- Ma phrase de ce tour est-elle plus proche de mon état que la précédente ?

C'est la boucle de feedback interne : Leia s'entend.
"""

from __future__ import annotations
import re, json, os, time, math
from collections import Counter, deque
from typing import Any, Dict, List, Optional, Tuple

try:
    import numpy as np
    _NUMPY = True
except ImportError:
    np = None  # type: ignore
    _NUMPY = False

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

# Mots parasites de remplissage (signalent une dérive vers le vague)
_FILLER_WORDS = {
    "chose","quelque","certain","sorte","manière","façon","genre","type",
    "aspect","point","question","réponse","moment","temps","fois","part",
    "niveau","sens","effet","résultat","suite","forme","base","fond",
    "continuité","résonance","appui","tension","présence","doute",
    "sentiment","impression","expérience","vécu","ressenti","état",
}

def _clamp(v, lo=0.0, hi=1.0):
    try: return max(lo, min(hi, float(v)))
    except: return lo

def _tokenize(text: str) -> List[str]:
    words = re.findall(r"[\wÀ-ÿ']{3,}", str(text or "").lower())
    return [w for w in words if w not in _STOP]


class TfIdfVectorizer:
    """
    Vectoriseur TF-IDF minimal, 100% Python/numpy.
    Construit un vocabulaire en ligne depuis les textes vus.
    """

    def __init__(self, max_features: int = 500):
        self.max_features = max_features
        self.vocab: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self._doc_count: int = 0
        self._df: Dict[str, int] = {}  # document frequency

    def fit_update(self, text: str):
        """Met à jour le vocabulaire avec un nouveau document."""
        words = set(_tokenize(text))
        self._doc_count += 1
        for w in words:
            self._df[w] = self._df.get(w, 0) + 1

    def _build_idf(self):
        N = max(self._doc_count, 1)
        self.idf = {
            w: math.log((N + 1) / (df + 1)) + 1.0
            for w, df in self._df.items()
        }

    def transform(self, text: str) -> Dict[str, float]:
        """Retourne un vecteur TF-IDF sparse (dict mot→poids)."""
        self._build_idf()
        words = _tokenize(text)
        if not words:
            return {}
        tf = Counter(words)
        total = len(words)
        vec = {}
        for w, cnt in tf.items():
            tfidf = (cnt / total) * self.idf.get(w, 1.0)
            vec[w] = tfidf
        return vec

    def cosine(self, vec_a: Dict[str, float], vec_b: Dict[str, float]) -> float:
        """Cosine similarity entre deux vecteurs sparses."""
        if not vec_a or not vec_b:
            return 0.0
        common = set(vec_a) & set(vec_b)
        dot = sum(vec_a[k] * vec_b[k] for k in common)
        norm_a = math.sqrt(sum(v*v for v in vec_a.values()))
        norm_b = math.sqrt(sum(v*v for v in vec_b.values()))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return _clamp(dot / (norm_a * norm_b))


class SemanticCoherence:
    """
    Mesure la cohérence sémantique de l'expression de Leia.

    Trois métriques principales :
    1. coherence_to_intent  : proximité entre ce qu'elle voulait dire et ce qu'elle a dit
    2. filler_ratio         : proportion de mots de remplissage (dérive vers le vague)
    3. drift_from_prev      : distance sémantique avec le tour précédent

    Ces métriques alimentent self_evaluation_loop pour corriger le prochain tour.
    """

    def __init__(self, storage_path: str = "data/semantic_coherence_default.json"):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(storage_path) if os.path.dirname(storage_path) else ".", exist_ok=True)
        self._vectorizer = TfIdfVectorizer(max_features=500)
        self._history: deque = deque(maxlen=20)
        self._intent_vectors: deque = deque(maxlen=10)  # vecteurs des intentions
        self._load()

    def _load(self):
        if not os.path.exists(self.storage_path): return
        try:
            with open(self.storage_path, encoding="utf-8") as f:
                data = json.load(f)
            # Recharger le vocabulaire TF-IDF
            self._vectorizer._doc_count = int(data.get("doc_count", 0))
            self._vectorizer._df = data.get("df", {})
            history_raw = data.get("history", [])
            for h in history_raw[-20:]:
                self._history.append(h)
        except Exception:
            pass

    def _save(self):
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump({
                    "doc_count": self._vectorizer._doc_count,
                    "df":        dict(list(self._vectorizer._df.items())[-800:]),
                    "history":   list(self._history)[-20:],
                    "timestamp": time.time(),
                }, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # ── Métriques ─────────────────────────────────────────────────────────────
    def measure_coherence(
        self,
        intended_concepts: List[str],
        response: str,
    ) -> Dict[str, Any]:
        """
        Mesure la cohérence entre l'intention (concepts actifs avant la réponse)
        et la réponse produite.

        intended_concepts : mots/concepts que Leia voulait exprimer
                           (depuis living_presence_stabilizer, focus, etc.)
        response          : la phrase finale produite
        """
        if not response:
            return {"coherence": 0.0, "filler_ratio": 1.0, "drift": 0.0,
                    "judgment": "vide"}

        # Mettre à jour le vocabulaire
        self._vectorizer.fit_update(response)
        if intended_concepts:
            intent_text = " ".join(intended_concepts)
            self._vectorizer.fit_update(intent_text)

        # Vecteurs
        resp_vec   = self._vectorizer.transform(response)
        intent_vec = self._vectorizer.transform(" ".join(intended_concepts)) if intended_concepts else {}

        # 1. Cohérence intention → réponse
        coherence = self._vectorizer.cosine(intent_vec, resp_vec) if intent_vec else 0.5

        # 2. Ratio de mots parasites
        resp_words = _tokenize(response)
        filler_count = sum(1 for w in resp_words if w in _FILLER_WORDS)
        filler_ratio = _clamp(filler_count / max(len(resp_words), 1))

        # 3. Dérive par rapport au tour précédent
        drift = 0.0
        if self._history:
            prev_vec = self._history[-1].get("vec", {})
            if prev_vec:
                sim = self._vectorizer.cosine(resp_vec, prev_vec)
                drift = _clamp(1.0 - sim)

        # 4. Richesse (diversité lexicale)
        unique_ratio = len(set(resp_words)) / max(len(resp_words), 1)

        # 5. Jugement qualitatif
        judgment = self._judge(coherence, filler_ratio, drift, unique_ratio)

        result = {
            "coherence":       round(coherence, 4),
            "filler_ratio":    round(filler_ratio, 4),
            "drift":           round(drift, 4),
            "unique_ratio":    round(unique_ratio, 4),
            "judgment":        judgment,
            "word_count":      len(resp_words),
            "concepts_matched": len(set(intended_concepts) & set(resp_words)),
        }

        # Historique
        self._history.append({
            "coherence":    result["coherence"],
            "filler_ratio": result["filler_ratio"],
            "drift":        result["drift"],
            "judgment":     judgment,
            "vec":          {k: round(v,4) for k,v in list(resp_vec.items())[:30]},
            "ts":           time.time(),
        })

        if len(self._history) % 5 == 0:
            self._save()

        return result

    def _judge(self, coherence: float, filler: float, drift: float,
               unique: float) -> str:
        """Jugement qualitatif de la réponse."""
        if coherence > 0.6 and filler < 0.2 and unique > 0.5:
            return "ancré"          # bien connecté à l'intention
        if filler > 0.5:
            return "vague"          # trop de mots de remplissage
        if drift > 0.7:
            return "dérive"         # rupture thématique
        if coherence < 0.2:
            return "découplé"       # déconnecté de l'intention
        if unique < 0.3:
            return "répétitif"      # peu de variété lexicale
        return "acceptable"

    # ── Analyse de ce que l'utilisateur dit ──────────────────────────────────
    def user_coherence_check(self, user_input: str,
                              prev_inputs: List[str]) -> Dict[str, Any]:
        """
        Vérifie la cohérence du message utilisateur avec le contexte.
        Utile pour détecter les changements brusques de sujet.
        """
        self._vectorizer.fit_update(user_input)
        user_vec = self._vectorizer.transform(user_input)

        if not prev_inputs:
            return {"topic_continuity": 1.0, "is_new_topic": False}

        prev_text = " ".join(prev_inputs[-3:])
        prev_vec  = self._vectorizer.transform(prev_text)
        sim = self._vectorizer.cosine(user_vec, prev_vec)

        return {
            "topic_continuity": round(sim, 4),
            "is_new_topic":    sim < 0.15,
            "shift_magnitude": round(1.0 - sim, 4),
        }

    # ── Détection de mots répétés ─────────────────────────────────────────────
    def repetition_analysis(self, recent_responses: List[str]) -> Dict[str, Any]:
        """
        Détecte les mots sur-utilisés dans les dernières réponses.
        Alimente le banned_set du weaver.
        """
        all_words: List[str] = []
        for r in recent_responses:
            all_words.extend(_tokenize(r))

        if not all_words:
            return {"overused": [], "repetition_score": 0.0}

        freq = Counter(all_words)
        total = len(all_words)
        n_responses = max(len(recent_responses), 1)

        # Sur-utilisé = apparaît dans >40% des réponses et >3 fois
        threshold_abs = max(3, n_responses * 0.4)
        overused = [
            {"word": w, "count": cnt, "freq": round(cnt/total, 3)}
            for w, cnt in freq.most_common(20)
            if cnt >= threshold_abs and w not in _FILLER_WORDS
        ]

        rep_score = _clamp(len(overused) / 10.0)
        return {
            "overused":          overused[:8],
            "repetition_score":  round(rep_score, 4),
            "total_words":       total,
            "unique_words":      len(set(all_words)),
        }

    # ── Signal pour le core ───────────────────────────────────────────────────
    def signal(self, intended_concepts: List[str],
               response: str,
               recent_responses: Optional[List[str]] = None) -> Dict[str, Any]:
        """Interface standard pour le core."""
        if not response:
            return {"available": False}

        coherence_data = self.measure_coherence(intended_concepts, response)
        rep_data = self.repetition_analysis(recent_responses or [])

        # Inhibitions à transmettre au weaver
        inhibitions = []
        if coherence_data["judgment"] == "vague":
            inhibitions.append("force_concrete_atoms")
        if coherence_data["judgment"] == "répétitif":
            inhibitions.append("structural_variation_required")
        if coherence_data["filler_ratio"] > 0.4:
            inhibitions.append("ban_filler_words")
        if coherence_data["drift"] > 0.6:
            inhibitions.append("return_to_focus")

        return {
            "available":       True,
            "coherence":       coherence_data["coherence"],
            "filler_ratio":    coherence_data["filler_ratio"],
            "drift":           coherence_data["drift"],
            "judgment":        coherence_data["judgment"],
            "word_count":      coherence_data["word_count"],
            "inhibitions":     inhibitions,
            "overused_words":  [x["word"] for x in rep_data["overused"]],
            "repetition_score": rep_data["repetition_score"],
        }

    def snapshot(self) -> Dict[str, Any]:
        if not self._history:
            return {"avg_coherence": 0.5, "history_len": 0}
        recent = list(self._history)[-5:]
        return {
            "avg_coherence":    round(sum(h["coherence"] for h in recent) / len(recent), 4),
            "avg_filler":       round(sum(h["filler_ratio"] for h in recent) / len(recent), 4),
            "last_judgment":    self._history[-1]["judgment"] if self._history else "",
            "history_len":      len(self._history),
        }