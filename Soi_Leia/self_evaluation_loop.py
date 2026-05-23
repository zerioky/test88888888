"""
self_evaluation_loop.py — V16
==============================
Boucle d'auto-évaluation de Leia.

Après chaque réponse, Leia s'évalue sur 4 critères :
  1. Pertinence — a-t-elle répondu à ce qui était demandé ?
  2. Répétition — a-t-elle répété quelque chose du tour précédent ?
  3. Parasites — un mot technique a-t-il passé les filtres ?
  4. Authenticité — la réponse venait-elle de son état réel ?

Le résultat n'efface pas ce qui a été dit.
Il ajuste le comportement au tour suivant via des signaux d'inhibition.

Aucune phrase préécrite. Aucun template de correction.
"""

from __future__ import annotations

import json
import os
import re
import time
from collections import deque
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(v)))


# Mots qui ne devraient jamais sortir en surface
_TECHNICAL_LEAK = {
    "pressure", "latent", "payload", "context", "signal", "engine",
    "weaver", "token", "score", "weight", "evidence", "field",
    "python", "json", "buffer", "debug", "sein", "auditifs",
    "metadata", "traceback", "snapshot", "label", "drive",
}

# Patterns de référence à soi-même sans contenu
_EMPTY_SELF_PATTERNS = [
    r"^je\s+\w+\s+je\s+\w+",   # "je X je Y" — répétition de structure
    r"\bje\b.{0,8}\bje\b",      # "je … je" trop rapprochés
]


# ---------------------------------------------------------------------------
# EvaluationReport
# ---------------------------------------------------------------------------

class EvaluationReport:
    def __init__(self) -> None:
        self.pertinence: float = 1.0     # 0 = hors sujet, 1 = pertinent
        self.repetition: float = 0.0     # 0 = pas de répétition, 1 = très répétitif
        self.parasites: List[str] = []   # mots techniques détectés
        self.authenticity: float = 1.0   # 0 = mécanique, 1 = depuis l'état réel
        self.too_short: bool = False      # réponse trop courte
        self.structural_loop: bool = False # même structure que le tour précédent
        self.overall_score: float = 1.0

    def compute_overall(self) -> float:
        self.overall_score = _clamp(
            self.pertinence * 0.35
            + (1.0 - self.repetition) * 0.25
            + (0 if self.parasites else 0.20)
            + self.authenticity * 0.20
        )
        return self.overall_score

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pertinence": round(self.pertinence, 3),
            "repetition": round(self.repetition, 3),
            "parasites": self.parasites,
            "authenticity": round(self.authenticity, 3),
            "too_short": self.too_short,
            "structural_loop": self.structural_loop,
            "overall_score": round(self.overall_score, 3),
        }


# ---------------------------------------------------------------------------
# SelfEvaluationLoop
# ---------------------------------------------------------------------------

class SelfEvaluationLoop:
    """
    Évalue les réponses de Leia et produit des signaux d'inhibition
    pour améliorer le tour suivant.
    """

    def __init__(self, storage_path: str = "data/self_eval_default.json", window: int = 6) -> None:
        self.storage_path = storage_path
        os.makedirs(os.path.dirname(storage_path) if os.path.dirname(storage_path) else ".", exist_ok=True)

        # Historique des évaluations récentes
        self.recent_reports: deque = deque(maxlen=window)
        # Inhibitions actives — transmises au weaver au prochain tour
        self.active_inhibitions: Dict[str, float] = {}
        # Mots récemment utilisés (à éviter)
        self.recent_surface_words: deque = deque(maxlen=window * 15)
        # Dernier score global
        self.last_score: float = 1.0

        self._load()

    # ------------------------------------------------------------------
    # Persistance légère
    # ------------------------------------------------------------------

    def _load(self) -> None:
        if not os.path.exists(self.storage_path):
            return
        try:
            with open(self.storage_path, encoding="utf-8") as f:
                data = json.load(f)
            self.active_inhibitions = data.get("active_inhibitions", {})
            self.recent_surface_words = deque(
                data.get("recent_surface_words", []), maxlen=90
            )
            self.last_score = data.get("last_score", 1.0)
        except Exception:
            pass

    def _save(self) -> None:
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump({
                    "active_inhibitions": self.active_inhibitions,
                    "recent_surface_words": list(self.recent_surface_words)[-60:],
                    "last_score": self.last_score,
                    "timestamp": time.time(),
                }, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Évaluation principale
    # ------------------------------------------------------------------

    def evaluate(
        self,
        user_input: str,
        response: str,
        previous_response: Optional[str] = None,
        emotional_state: Optional[Any] = None,
    ) -> EvaluationReport:
        """
        Évalue la réponse et met à jour les inhibitions pour le prochain tour.
        """
        report = EvaluationReport()

        if not response or not response.strip():
            report.overall_score = 0.0
            return report

        r_lower = response.lower()
        r_words = re.findall(r"[a-zàâéèêëîïôùûüç]+", r_lower)

        # 1. Pertinence — les mots-clés de la question sont-ils reflétés ?
        q_words = set(re.findall(r"[a-zàâéèêëîïôùûüç]{4,}", user_input.lower()))
        if q_words:
            overlap = sum(1 for w in q_words if w in r_lower) / len(q_words)
            report.pertinence = _clamp(0.4 + overlap * 0.6)
        else:
            report.pertinence = 0.7

        # 2. Répétition par rapport au tour précédent
        if previous_response:
            prev_words = set(re.findall(r"[a-zàâéèêëîïôùûüç]{5,}", previous_response.lower()))
            curr_words = set(re.findall(r"[a-zàâéèêëîïôùûüç]{5,}", r_lower))
            if prev_words:
                overlap_ratio = len(prev_words & curr_words) / max(len(prev_words), 1)
                report.repetition = _clamp(overlap_ratio * 1.4)
            # Détecter même structure de début de phrase
            prev_start = previous_response[:25].lower()
            curr_start = response[:25].lower()
            if prev_start[:12] == curr_start[:12]:
                report.structural_loop = True
                report.repetition = _clamp(report.repetition + 0.3)

        # 3. Parasites techniques
        for word in r_words:
            if word in _TECHNICAL_LEAK:
                report.parasites.append(word)

        # 4. Trop court
        report.too_short = len(response.strip()) < 18

        # 5. Boucle structurelle interne
        for pattern in _EMPTY_SELF_PATTERNS:
            if re.search(pattern, r_lower):
                report.structural_loop = True
                break

        # 6. Authenticité — basée sur l'état émotionnel réel
        if emotional_state is not None:
            try:
                tension = float(getattr(emotional_state, "tension", 0.5))
                fatigue = float(getattr(emotional_state, "fatigue", 0.3))
                # Si tension haute mais réponse sans mots de tension → peu authentique
                tension_words = {"tension", "résiste", "poids", "lourd", "difficile", "retiens"}
                if tension > 0.55 and not any(w in r_lower for w in tension_words):
                    report.authenticity = _clamp(1.0 - tension * 0.5)
            except Exception:
                pass

        # Score global
        report.compute_overall()
        self.last_score = report.overall_score
        self.recent_reports.append(report.to_dict())

        # Enregistrer les mots utilisés
        for w in r_words:
            if len(w) > 4:
                self.recent_surface_words.append(w)

        # Mettre à jour les inhibitions
        self._update_inhibitions(report)
        self._save()

        return report

    # ------------------------------------------------------------------
    # Inhibitions
    # ------------------------------------------------------------------

    def _update_inhibitions(self, report: EvaluationReport) -> None:
        """
        Traduit le rapport en inhibitions concrètes pour le weaver.
        """
        # Décroissance naturelle des inhibitions existantes
        for key in list(self.active_inhibitions.keys()):
            self.active_inhibitions[key] = _clamp(self.active_inhibitions[key] * 0.7)
            if self.active_inhibitions[key] < 0.05:
                del self.active_inhibitions[key]

        # Si répétition élevée → inhiber les mots trop récents
        if report.repetition > 0.35:
            self.active_inhibitions["repetition_inhibition"] = _clamp(report.repetition * 1.2)

        # Si parasites → inhibition forte des mots techniques
        if report.parasites:
            self.active_inhibitions["technical_leak_inhibition"] = 0.9

        # Si boucle structurelle → forcer variation
        if report.structural_loop:
            self.active_inhibitions["structural_variation_required"] = 0.8

        # Si trop court → pousser vers plus d'expression
        if report.too_short:
            self.active_inhibitions["expression_pressure_boost"] = 0.6

        # Si peu pertinent → renforcer le lien à la question
        if report.pertinence < 0.45:
            self.active_inhibitions["pertinence_required"] = 0.7

    def get_inhibition_signal(self) -> Dict[str, Any]:
        """
        Signal transmis au weaver et au core pour le prochain tour.
        """
        # Mots récents à éviter
        word_freq: Dict[str, int] = {}
        for w in self.recent_surface_words:
            word_freq[w] = word_freq.get(w, 0) + 1
        overused = [w for w, c in word_freq.items() if c >= 3]

        return {
            "available": True,
            "inhibitions": dict(self.active_inhibitions),
            "overused_words": overused[:20],
            "last_score": round(self.last_score, 3),
            "structural_variation": self.active_inhibitions.get("structural_variation_required", 0.0) > 0.3,
            "repetition_pressure": self.active_inhibitions.get("repetition_inhibition", 0.0),
            "boost_expression": self.active_inhibitions.get("expression_pressure_boost", 0.0) > 0.3,
        }

    def average_score(self) -> float:
        if not self.recent_reports:
            return 1.0
        return sum(r.get("overall_score", 1.0) for r in self.recent_reports) / len(self.recent_reports)
