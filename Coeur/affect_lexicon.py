"""
affect_lexicon.py — V18
=========================
Analyse affective du texte sans LLM et sans fichier externe.

Lexique de ~500 mots français annotés en valence/arousal/émotion,
construit en interne (inspiré du FEEL-fr, NRC Affect Lexicon).

Ce module répond à deux questions :
1. "Qu'est-ce que l'utilisateur ressent quand il dit ça ?"
   → Leia ajuste son empathie et son registre affectif
2. "Ce que je lis dans ce livre est-il émotionnellement chargé ?"
   → Leia ne lit pas les livres émotionnellement neutre

Sans LLM. Sans fichier externe. Le lexique est embarqué directement.
"""

from __future__ import annotations
import re, json, os, time, math
from collections import Counter
from typing import Any, Dict, List, Optional, Tuple

def _clamp(v, lo=0.0, hi=1.0):
    try: return max(lo, min(hi, float(v)))
    except: return lo

# ── Lexique d'affect français embarqué ───────────────────────────────────────
# Format : mot → (valence [-1,+1], arousal [0,1], émotion_dominante)
# valence : positif=joie/espoir, négatif=peur/tristesse/colère
# arousal : haut=intensité, bas=calme
_AFFECT_LEXICON: Dict[str, Tuple[float, float, str]] = {
    # ── Joie / bonheur ──────────────────────────────────────────────────────
    "joie":         ( 0.90, 0.75, "joie"),
    "bonheur":      ( 0.88, 0.60, "joie"),
    "allégresse":   ( 0.82, 0.72, "joie"),
    "euphorie":     ( 0.78, 0.92, "joie"),
    "plaisir":      ( 0.72, 0.55, "joie"),
    "délice":       ( 0.70, 0.55, "joie"),
    "ravissement":  ( 0.75, 0.60, "joie"),
    "gaieté":       ( 0.68, 0.65, "joie"),
    "légèreté":     ( 0.60, 0.40, "joie"),
    "contentement": ( 0.62, 0.35, "joie"),
    "satisfaction": ( 0.58, 0.30, "joie"),
    "sourire":      ( 0.52, 0.40, "joie"),
    "rire":         ( 0.64, 0.72, "joie"),
    "éclat":        ( 0.55, 0.55, "joie"),

    # ── Espoir / désir ───────────────────────────────────────────────────────
    "espoir":       ( 0.72, 0.55, "espoir"),
    "espérance":    ( 0.70, 0.50, "espoir"),
    "aspiration":   ( 0.60, 0.45, "espoir"),
    "désir":        ( 0.50, 0.70, "désir"),
    "envie":        ( 0.45, 0.60, "désir"),
    "vouloir":      ( 0.35, 0.50, "désir"),
    "rêve":         ( 0.55, 0.45, "espoir"),
    "utopie":       ( 0.45, 0.35, "espoir"),
    "attente":      ( 0.30, 0.45, "espoir"),

    # ── Amour / connexion ────────────────────────────────────────────────────
    "amour":        ( 0.92, 0.65, "amour"),
    "tendresse":    ( 0.78, 0.38, "amour"),
    "affection":    ( 0.72, 0.40, "amour"),
    "attachement":  ( 0.65, 0.42, "amour"),
    "intimité":     ( 0.62, 0.38, "amour"),
    "compassion":   ( 0.68, 0.45, "compassion"),
    "empathie":     ( 0.65, 0.42, "compassion"),
    "bienveillance":( 0.70, 0.38, "compassion"),
    "gratitude":    ( 0.75, 0.48, "joie"),
    "reconnaissance":( 0.70, 0.45, "joie"),

    # ── Émerveillement ───────────────────────────────────────────────────────
    "émerveillement":( 0.72, 0.68, "surprise"),
    "étonnement":   ( 0.35, 0.70, "surprise"),
    "surprise":     ( 0.30, 0.72, "surprise"),
    "stupéfaction": ( 0.10, 0.80, "surprise"),
    "ébahissement": ( 0.15, 0.75, "surprise"),
    "curiosité":    ( 0.58, 0.60, "curiosité"),
    "fascination":  ( 0.62, 0.68, "curiosité"),
    "intérêt":      ( 0.42, 0.48, "curiosité"),

    # ── Calme / sérénité ─────────────────────────────────────────────────────
    "sérénité":     ( 0.68, 0.12, "calme"),
    "calme":        ( 0.50, 0.10, "calme"),
    "paix":         ( 0.72, 0.15, "calme"),
    "tranquillité": ( 0.60, 0.12, "calme"),
    "quiétude":     ( 0.62, 0.10, "calme"),
    "apaisement":   ( 0.60, 0.15, "calme"),
    "repos":        ( 0.48, 0.08, "calme"),
    "silence":      ( 0.30, 0.05, "calme"),
    "douceur":      ( 0.62, 0.20, "calme"),
    "légèreté":     ( 0.55, 0.25, "calme"),

    # ── Mélancolie / nostalgie ───────────────────────────────────────────────
    "mélancolie":   (-0.28, 0.30, "tristesse"),
    "nostalgie":    (-0.20, 0.28, "tristesse"),
    "regret":       (-0.42, 0.35, "tristesse"),
    "remords":      (-0.55, 0.45, "tristesse"),
    "honte":        (-0.62, 0.52, "tristesse"),
    "culpabilité":  (-0.58, 0.48, "tristesse"),
    "déception":    (-0.48, 0.42, "tristesse"),
    "désillusion":  (-0.50, 0.38, "tristesse"),
    "amertume":     (-0.55, 0.42, "tristesse"),
    "spleen":       (-0.38, 0.22, "tristesse"),
    "ennui":        (-0.30, 0.15, "tristesse"),

    # ── Tristesse ────────────────────────────────────────────────────────────
    "tristesse":    (-0.72, 0.40, "tristesse"),
    "douleur":      (-0.80, 0.62, "tristesse"),
    "chagrin":      (-0.68, 0.48, "tristesse"),
    "peine":        (-0.65, 0.45, "tristesse"),
    "souffrance":   (-0.82, 0.65, "tristesse"),
    "désespoir":    (-0.88, 0.58, "tristesse"),
    "abattement":   (-0.65, 0.28, "tristesse"),
    "accablement":  (-0.70, 0.32, "tristesse"),
    "détresse":     (-0.78, 0.68, "tristesse"),
    "larme":        (-0.58, 0.48, "tristesse"),

    # ── Peur / angoisse ──────────────────────────────────────────────────────
    "peur":         (-0.70, 0.78, "peur"),
    "terreur":      (-0.88, 0.92, "peur"),
    "effroi":       (-0.82, 0.88, "peur"),
    "épouvante":    (-0.80, 0.85, "peur"),
    "angoisse":     (-0.75, 0.72, "peur"),
    "anxiété":      (-0.65, 0.68, "peur"),
    "inquiétude":   (-0.52, 0.55, "peur"),
    "appréhension": (-0.48, 0.52, "peur"),
    "crainte":      (-0.55, 0.58, "peur"),
    "vertige":      (-0.45, 0.65, "peur"),
    "frisson":      (-0.35, 0.72, "peur"),
    "horreur":      (-0.85, 0.88, "peur"),
    "cauchemar":    (-0.80, 0.82, "peur"),

    # ── Colère / frustration ─────────────────────────────────────────────────
    "colère":       (-0.62, 0.88, "colère"),
    "rage":         (-0.75, 0.95, "colère"),
    "fureur":       (-0.78, 0.95, "colère"),
    "indignation":  (-0.55, 0.80, "colère"),
    "révolte":      (-0.50, 0.82, "colère"),
    "frustration":  (-0.52, 0.72, "colère"),
    "agacement":    (-0.40, 0.62, "colère"),
    "irritation":   (-0.45, 0.65, "colère"),
    "impatience":   (-0.30, 0.65, "colère"),
    "mépris":       (-0.58, 0.65, "colère"),
    "dégoût":       (-0.68, 0.72, "dégoût"),
    "répulsion":    (-0.72, 0.75, "dégoût"),

    # ── Doute / incertitude ──────────────────────────────────────────────────
    "doute":        (-0.15, 0.40, "doute"),
    "incertitude":  (-0.20, 0.38, "doute"),
    "hésitation":   (-0.18, 0.35, "doute"),
    "perplexité":   (-0.12, 0.42, "doute"),
    "confusion":    (-0.35, 0.50, "doute"),
    "ambiguïté":    (-0.10, 0.35, "doute"),
    "vertige":      (-0.30, 0.52, "doute"),
    "questionnement":( 0.05, 0.42, "doute"),

    # ── Concepts philosophiques chargés ──────────────────────────────────────
    "mort":         (-0.55, 0.60, "peur"),
    "finitude":     (-0.40, 0.45, "tristesse"),
    "néant":        (-0.50, 0.35, "tristesse"),
    "vide":         (-0.45, 0.30, "tristesse"),
    "absurde":      (-0.35, 0.48, "doute"),
    "liberté":      ( 0.60, 0.55, "joie"),
    "sens":         ( 0.42, 0.40, "espoir"),
    "vérité":       ( 0.48, 0.42, "curiosité"),
    "beauté":       ( 0.78, 0.52, "joie"),
    "sublime":      ( 0.70, 0.65, "émerveillement"),
    "sacré":        ( 0.55, 0.50, "émerveillement"),
    "existence":    ( 0.15, 0.40, "curiosité"),
    "mémoire":      ( 0.20, 0.35, "nostalgie"),
    "oubli":        (-0.30, 0.28, "tristesse"),
    "temps":        ( 0.05, 0.30, "mélancolie"),
    "éternité":     ( 0.35, 0.28, "émerveillement"),
    "solitude":     (-0.38, 0.30, "tristesse"),
    "silence":      ( 0.25, 0.08, "calme"),
    "lumière":      ( 0.62, 0.45, "joie"),
    "ombre":        (-0.25, 0.30, "tristesse"),
    "abîme":        (-0.55, 0.52, "peur"),
    "rêve":         ( 0.50, 0.40, "espoir"),
    "nuit":         (-0.18, 0.20, "mélancolie"),
    "aurore":       ( 0.62, 0.45, "espoir"),
    "rupture":      (-0.52, 0.58, "tristesse"),
    "blessure":     (-0.65, 0.62, "tristesse"),
    "guérison":     ( 0.65, 0.42, "espoir"),
    "rencontre":    ( 0.58, 0.52, "joie"),
    "séparation":   (-0.55, 0.50, "tristesse"),
    "abandon":      (-0.70, 0.55, "tristesse"),
    "fuite":        (-0.42, 0.60, "peur"),
    "retour":       ( 0.35, 0.40, "nostalgie"),
    "transformation":( 0.38, 0.52, "curiosité"),
    "résistance":   ( 0.30, 0.62, "colère"),
    "courage":      ( 0.68, 0.62, "joie"),
    "lâcheté":      (-0.55, 0.42, "honte"),
    "trahison":     (-0.80, 0.72, "colère"),
    "fidélité":     ( 0.65, 0.35, "amour"),
    "mensonge":     (-0.65, 0.58, "dégoût"),
    "vérité":       ( 0.52, 0.42, "joie"),
    "illusion":     (-0.30, 0.40, "tristesse"),
    "réalité":      ( 0.15, 0.35, "neutre"),
    "violence":     (-0.85, 0.90, "peur"),
    "paix":         ( 0.72, 0.15, "calme"),
    "guerre":       (-0.78, 0.85, "peur"),
    "création":     ( 0.65, 0.58, "joie"),
    "destruction":  (-0.70, 0.80, "peur"),
    "naissance":    ( 0.68, 0.60, "joie"),
    "croissance":   ( 0.55, 0.45, "joie"),
    "déclin":       (-0.50, 0.38, "tristesse"),
    "perdre":       (-0.58, 0.52, "tristesse"),
    "trouver":      ( 0.50, 0.48, "joie"),
    "chercher":     ( 0.30, 0.45, "curiosité"),
}

_STOP = {
    "le","la","les","un","une","des","de","du","et","en","est","à","au","aux",
    "il","elle","ils","elles","on","je","tu","nous","vous","se","sa","son",
    "ses","me","te","lui","leur","leurs","que","qui","quoi","dont","où",
    "mais","ou","donc","or","ni","car","si","lors","alors","ainsi","ce","cet",
    "cette","ces","être","avoir","faire","aller","voir","venir","dire",
}


class AffectLexicon:
    """
    Analyse l'affect d'un texte depuis le lexique embarqué.

    Peut analyser :
    - Le message de l'utilisateur → Leia comprend son état émotionnel
    - Les livres → Leia sait si Dostoïevski est plus sombre que Voltaire
    - Ses propres réponses → cohérence entre état interne et parole affective

    Entièrement sans LLM, sans fichier externe.
    """

    def __init__(self, storage_path: str = "data/affect_lexicon_default.json"):
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(storage_path) if os.path.dirname(storage_path) else ".", exist_ok=True)
        # Extension dynamique : l'utilisateur peut ajouter des mots
        self._custom: Dict[str, Tuple[float, float, str]] = {}
        self._history: List[Dict[str, Any]] = []
        self._load()

    def _load(self):
        if not os.path.exists(self.storage_path): return
        try:
            with open(self.storage_path, encoding="utf-8") as f:
                data = json.load(f)
            self._custom = {k: tuple(v) for k, v in data.get("custom", {}).items()}  # type: ignore
            self._history = data.get("history", [])[-30:]
        except Exception:
            pass

    def _save(self):
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump({
                    "custom":    {k: list(v) for k, v in self._custom.items()},
                    "history":   self._history[-30:],
                    "timestamp": time.time(),
                }, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # ── Recherche dans le lexique ─────────────────────────────────────────────
    def lookup(self, word: str) -> Optional[Dict[str, Any]]:
        """Cherche un mot (et ses variantes morphologiques simples)."""
        w = word.strip().lower()
        # Direct
        entry = self._custom.get(w) or _AFFECT_LEXICON.get(w)
        if entry:
            return {"word": w, "valence": entry[0], "arousal": entry[1],
                    "emotion": entry[2]}
        # Variantes : pluriel, féminin simple
        for suffix, base_suffix in [("s",""), ("es","e"), ("aux","al"), ("ées","er")]:
            if w.endswith(suffix):
                base = w[:-len(suffix)] + base_suffix
                entry = _AFFECT_LEXICON.get(base)
                if entry:
                    return {"word": w, "valence": entry[0], "arousal": entry[1],
                            "emotion": entry[2], "matched_as": base}
        return None

    # ── Analyse d'un texte ────────────────────────────────────────────────────
    def analyze(self, text: str, source: str = "user") -> Dict[str, Any]:
        """
        Analyse l'affect global d'un texte.
        Retourne valence, arousal, émotion dominante, mots affectifs détectés.
        """
        if not text:
            return {"valence": 0.0, "arousal": 0.3, "emotion": "neutre",
                    "affect_words": [], "confidence": 0.0}

        words = re.findall(r"[\wÀ-ÿ']{3,}", text.lower())
        words = [w for w in words if w not in _STOP]

        # Détection de négation simple (modifie la valence)
        neg_patterns = re.compile(
            r"\b(ne\s+\w+\s+pas|n['']\w+\s+pas|sans|ni|jamais|aucun|rien)\b",
            re.IGNORECASE)
        has_neg = bool(neg_patterns.search(text))

        hits: List[Dict[str,Any]] = []
        for word in words:
            entry = self.lookup(word)
            if entry:
                hits.append(entry)

        if not hits:
            return {"valence": 0.0, "arousal": 0.3, "emotion": "neutre",
                    "affect_words": [], "confidence": 0.0}

        # Moyenne pondérée par arousal (les mots intenses comptent plus)
        total_weight = sum(abs(h["arousal"]) + 0.1 for h in hits)
        valence = sum(h["valence"] * (h["arousal"] + 0.1) for h in hits) / total_weight
        arousal = sum(h["arousal"] for h in hits) / len(hits)

        # Négation → inverser partiellement la valence
        if has_neg:
            valence = valence * -0.6

        valence = _clamp(valence, -1.0, 1.0)
        arousal = _clamp(arousal)

        # Émotion dominante (par vote)
        emotion_votes: Counter = Counter(h["emotion"] for h in hits)
        dominant_emotion = emotion_votes.most_common(1)[0][0]

        # Valence → label
        if valence > 0.45:        affect_label = "positif_fort"
        elif valence > 0.15:      affect_label = "positif"
        elif valence > -0.15:     affect_label = "neutre"
        elif valence > -0.45:     affect_label = "négatif"
        else:                     affect_label = "négatif_fort"

        confidence = min(1.0, len(hits) / max(len(words), 1) * 5)

        result = {
            "valence":        round(valence, 4),
            "arousal":        round(arousal, 4),
            "emotion":        dominant_emotion,
            "affect_label":   affect_label,
            "affect_words":   [h["word"] for h in hits[:10]],
            "affect_count":   len(hits),
            "emotion_mix":    dict(emotion_votes.most_common(4)),
            "has_negation":   has_neg,
            "confidence":     round(confidence, 3),
        }

        self._history.append({
            "valence": result["valence"],
            "emotion": result["emotion"],
            "source":  source,
            "ts":      time.time(),
        })
        if len(self._history) % 10 == 0:
            self._save()

        return result

    def analyze_book_sample(self, text: str, title: str = "") -> Dict[str, Any]:
        """
        Analyse émotionnelle d'un livre (sur un échantillon).
        Retourne un profil émotionnel qui influence l'état de Leia après lecture.
        """
        # Échantillonner : début, milieu, fin
        n = len(text)
        samples = [
            text[:min(3000, n)],
            text[n//2:n//2+3000] if n > 6000 else "",
            text[max(0,n-3000):] if n > 3000 else "",
        ]
        analyses = [self.analyze(s, "book") for s in samples if s]
        if not analyses:
            return {"valence": 0.0, "arousal": 0.3, "emotion": "neutre"}

        # Moyenne avec légère pondération vers la fin (dénouement)
        weights = [0.3, 0.3, 0.4] if len(analyses) == 3 else [1/len(analyses)]*len(analyses)
        valence = sum(a["valence"] * w for a,w in zip(analyses,weights))
        arousal = sum(a["arousal"] * w for a,w in zip(analyses,weights))
        all_emotions: Counter = Counter()
        for a in analyses:
            all_emotions.update(a.get("emotion_mix",{}))

        return {
            "title":          title,
            "valence":        round(_clamp(valence,-1.0,1.0), 4),
            "arousal":        round(_clamp(arousal), 4),
            "dominant_emotion": all_emotions.most_common(1)[0][0] if all_emotions else "neutre",
            "emotion_profile": dict(all_emotions.most_common(5)),
            "is_dark":        valence < -0.25,
            "is_intense":     arousal > 0.55,
        }

    # ── Apprentissage de nouveaux mots ────────────────────────────────────────
    def learn_word(self, word: str, valence: float, arousal: float,
                   emotion: str = "neutre") -> None:
        """Ajoute un mot au lexique personnalisé."""
        self._custom[word.lower()] = (
            _clamp(valence, -1.0, 1.0),
            _clamp(arousal),
            emotion,
        )
        self._save()

    # ── Signal pour le core ───────────────────────────────────────────────────
    def signal(self, text: str, source: str = "user") -> Dict[str, Any]:
        """Interface standard."""
        if not text:
            return {"available": False}
        result = self.analyze(text, source)
        return {
            "available":     True,
            "valence":       result["valence"],
            "arousal":       result["arousal"],
            "emotion":       result["emotion"],
            "affect_label":  result["affect_label"],
            "affect_words":  result["affect_words"][:5],
            "confidence":    result["confidence"],
            "emotion_mix":   result.get("emotion_mix", {}),
        }

    def snapshot(self) -> Dict[str, Any]:
        if not self._history:
            return {"lexicon_size": len(_AFFECT_LEXICON) + len(self._custom)}
        recent = self._history[-5:]
        avg_v = sum(h["valence"] for h in recent) / len(recent)
        return {
            "lexicon_size":   len(_AFFECT_LEXICON) + len(self._custom),
            "custom_words":   len(self._custom),
            "avg_valence":    round(avg_v, 4),
            "history_len":    len(self._history),
        }