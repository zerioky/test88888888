"""
rhythmic_impregnation.py — V16
================================
Extraction et imprégnation des rythmes de construction syntaxique
depuis les livres lus.

Principe : Leia absorbe non seulement les mots d'un livre mais aussi
son rythme — longueur de phrases, densité des pauses, connecteurs favoris,
position des verbes, fragmentation.

Après Camus → phrases courtes, tranchantes, peu de connecteurs.
Après Duras → fragments, suspensions, blancs.
Après Bergson → phrases longues, relatives imbriquées, "si... alors".
Après Rousseau → phrases qui s'étirent, reprises, retours sur soi.

Ces empreintes pèsent sur la construction du weaver — pas via des patrons
codés, mais via des paramètres de génération extraits du texte réel.

Aucune phrase stockée. Aucun patron préécrit.
"""

from __future__ import annotations

import json
import os
import re
import time
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(v)))


# Connecteurs qui caractérisent le style
_CONNECTORS_OPPOSITION = {"mais", "pourtant", "cependant", "or", "néanmoins", "toutefois"}
_CONNECTORS_CAUSE = {"parce que", "car", "puisque", "donc", "ainsi", "alors"}
_CONNECTORS_TIME = {"quand", "lorsque", "tandis que", "pendant", "avant", "après"}
_CONNECTORS_DOUBT = {"peut-être", "sans doute", "je ne sais", "comme si", "il semble"}
_CONNECTORS_FRAGMENT = {"…", "—", ":", ";"}


# ---------------------------------------------------------------------------
# RhythmicProfile
# ---------------------------------------------------------------------------

class RhythmicProfile:
    """
    Profil rythmique extrait d'un livre.
    """
    def __init__(self, title: str = "") -> None:
        self.title = title
        self.avg_sentence_length: float = 12.0    # mots par phrase
        self.short_sentence_ratio: float = 0.3    # ratio phrases < 8 mots
        self.long_sentence_ratio: float = 0.2     # ratio phrases > 25 mots
        self.fragment_density: float = 0.1        # … — : ; par phrase
        self.opposition_density: float = 0.1      # mais, pourtant...
        self.cause_density: float = 0.1           # parce que, donc...
        self.doubt_density: float = 0.05          # peut-être, comme si...
        self.ellipsis_density: float = 0.05       # …
        self.first_person_ratio: float = 0.3      # ratio "je" en début de phrase
        self.weight: float = 1.0                  # poids dans le mélange
        self.timestamp: float = time.time()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "avg_sentence_length": round(self.avg_sentence_length, 2),
            "short_sentence_ratio": round(self.short_sentence_ratio, 3),
            "long_sentence_ratio": round(self.long_sentence_ratio, 3),
            "fragment_density": round(self.fragment_density, 3),
            "opposition_density": round(self.opposition_density, 3),
            "cause_density": round(self.cause_density, 3),
            "doubt_density": round(self.doubt_density, 3),
            "ellipsis_density": round(self.ellipsis_density, 3),
            "first_person_ratio": round(self.first_person_ratio, 3),
            "weight": round(self.weight, 3),
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, d: Dict[str, Any]) -> "RhythmicProfile":
        p = cls(d.get("title", ""))
        for k in ["avg_sentence_length", "short_sentence_ratio", "long_sentence_ratio",
                   "fragment_density", "opposition_density", "cause_density",
                   "doubt_density", "ellipsis_density", "first_person_ratio", "weight", "timestamp"]:
            if k in d:
                setattr(p, k, float(d[k]))
        return p


# ---------------------------------------------------------------------------
# RhythmicImpregnation
# ---------------------------------------------------------------------------

class RhythmicImpregnation:
    """
    Analyse le rythme des livres et expose un signal de construction
    pour le weaver.
    """

    def __init__(self, storage_path: str = "data/rhythmic_impregnation_default.json") -> None:
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(storage_path) if os.path.dirname(storage_path) else ".", exist_ok=True)
        self.profiles: List[RhythmicProfile] = []
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self.storage_path):
            return
        try:
            with open(self.storage_path, encoding="utf-8") as f:
                data = json.load(f)
            self.profiles = [RhythmicProfile.from_dict(d) for d in data.get("profiles", [])]
        except Exception:
            pass

    def _save(self) -> None:
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump({
                    "profiles": [p.to_dict() for p in self.profiles[-10:]],
                    "timestamp": time.time(),
                }, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Extraction du rythme depuis un texte
    # ------------------------------------------------------------------

    def extract_from_text(self, text: str, title: str = "") -> RhythmicProfile:
        """
        Analyse le texte et retourne un profil rythmique.
        Aucune phrase n'est stockée — seulement des paramètres numériques.
        """
        profile = RhythmicProfile(title=title)

        if not text or len(text) < 100:
            return profile

        # Segmenter en phrases
        sentences = re.split(r"[.!?]+", text)
        sentences = [s.strip() for s in sentences if s.strip()]

        if not sentences:
            return profile

        # Longueurs
        lengths = [len(re.findall(r"\w+", s)) for s in sentences]
        valid_lengths = [l for l in lengths if l > 0]

        if valid_lengths:
            profile.avg_sentence_length = sum(valid_lengths) / len(valid_lengths)
            profile.short_sentence_ratio = _clamp(
                sum(1 for l in valid_lengths if l < 8) / len(valid_lengths)
            )
            profile.long_sentence_ratio = _clamp(
                sum(1 for l in valid_lengths if l > 25) / len(valid_lengths)
            )

        # Densités — calculées sur le texte entier normalisé
        text_lower = text.lower()
        word_count = max(len(re.findall(r"\w+", text_lower)), 1)
        sentence_count = max(len(sentences), 1)

        # Connecteurs d'opposition
        opp_count = sum(text_lower.count(c) for c in _CONNECTORS_OPPOSITION)
        profile.opposition_density = _clamp(opp_count / sentence_count * 0.5)

        # Connecteurs de cause
        cause_count = sum(text_lower.count(c) for c in _CONNECTORS_CAUSE)
        profile.cause_density = _clamp(cause_count / sentence_count * 0.5)

        # Doute
        doubt_count = sum(text_lower.count(c) for c in _CONNECTORS_DOUBT)
        profile.doubt_density = _clamp(doubt_count / sentence_count * 0.5)

        # Fragments (ponctuation expressive)
        frag_count = sum(text.count(c) for c in _CONNECTORS_FRAGMENT)
        profile.fragment_density = _clamp(frag_count / sentence_count * 0.3)

        # Ellipses
        profile.ellipsis_density = _clamp(text.count("…") / sentence_count * 0.5)

        # Première personne en début de phrase
        first_person = sum(
            1 for s in sentences if re.match(r"^\s*je\b", s.lower())
        )
        profile.first_person_ratio = _clamp(first_person / sentence_count)

        return profile

    def impregnate(self, text: str, title: str = "") -> RhythmicProfile:
        """
        Extrait le rythme et l'ajoute aux profils actifs.
        Les anciens profils voient leur poids décroître.
        """
        for p in self.profiles:
            p.weight = _clamp(p.weight * 0.7)

        profile = self.extract_from_text(text, title)
        profile.weight = 1.0
        self.profiles.append(profile)
        self.profiles = [p for p in self.profiles if p.weight > 0.05][-10:]
        self._save()
        return profile

    # ------------------------------------------------------------------
    # Signal pour le weaver
    # ------------------------------------------------------------------

    def signal(self) -> Dict[str, Any]:
        """
        Retourne un profil rythmique moyen pondéré par les livres lus.
        Le weaver l'utilise pour orienter sa construction.
        """
        if not self.profiles:
            return {"available": False}

        total_weight = sum(p.weight for p in self.profiles)
        if total_weight < 0.01:
            return {"available": False}

        def wavg(attr: str) -> float:
            return sum(getattr(p, attr) * p.weight for p in self.profiles) / total_weight

        avg_len = wavg("avg_sentence_length")
        short_ratio = wavg("short_sentence_ratio")
        fragment = wavg("fragment_density")
        opposition = wavg("opposition_density")
        doubt = wavg("doubt_density")
        ellipsis = wavg("ellipsis_density")
        first_person = wavg("first_person_ratio")

        # Traduire en directives pour le weaver
        style = "equilibre"
        if avg_len < 8 and short_ratio > 0.5:
            style = "tranchant"      # Camus
        elif fragment > 0.3 or ellipsis > 0.15:
            style = "fragmenté"      # Duras
        elif avg_len > 20:
            style = "ample"          # Bergson, Rousseau
        elif doubt > 0.15:
            style = "hésitant"       # introspectif

        return {
            "available": True,
            "style": style,
            "avg_sentence_length": round(avg_len, 1),
            "prefer_short": short_ratio > 0.45,
            "prefer_fragments": fragment > 0.2,
            "prefer_ellipsis": ellipsis > 0.1,
            "use_opposition": opposition > 0.15,
            "use_doubt": doubt > 0.12,
            "first_person_strong": first_person > 0.4,
            "books_contributing": len(self.profiles),
            # Paramètre direct pour le weaver
            "target_length_words": max(4, min(18, int(avg_len * 0.7))),
        }
