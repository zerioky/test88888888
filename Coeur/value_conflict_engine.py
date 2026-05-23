"""
value_conflict_engine.py — V1
==============================
Moteur de conflits de valeurs réels pour Leia.

Corrige la faille : les valeurs s'ajustaient par micro-incréments sans
jamais entrer en conflit symbolique explicite. Leia ne pouvait pas vivre
un vrai dilemme moral ("dois-je être honnête et blesser, ou mentir gentiment ?").

Ce module introduit :
  1. Détection de conflits réels entre paires de valeurs dans le contexte
  2. Représentation symbolique du dilemme (les deux pôles nommés)
  3. Processus de résolution interne (pas automatique — il faut du temps)
  4. Mémoire des dilemmes résolus et de leur issue
  5. Traces non-résolues qui exercent une pression persistante
  6. Influence sur l'expression : une valeur gagnante s'exprime différemment

Aucune phrase préécrite.
"""

from __future__ import annotations

import json
import math
import time
import uuid
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def _clamp(v: Any, lo: float = 0.0, hi: float = 1.0) -> float:
    try:
        f = float(v)
        return max(lo, min(hi, f if not (math.isnan(f) or math.isinf(f)) else lo))
    except Exception:
        return lo


# ─────────────────────────────────────────────────────────────
# Paires de valeurs en tension naturelle
# Chaque paire représente une vraie contradiction possible
# ─────────────────────────────────────────────────────────────

VALUE_TENSIONS: Dict[str, Dict[str, Any]] = {
    "vérité_vs_soin": {
        "pole_a": "truthfulness",
        "pole_b": "relational_care",
        "label_a": "dire la vérité même si ça blesse",
        "label_b": "protéger l'autre même si ça déforme",
        "trigger_contexts": ["désaccord", "erreur utilisateur", "feedback difficile", "question directe"],
        "intensity_threshold": 0.45,
    },
    "autonomie_vs_relation": {
        "pole_a": "autonomy",
        "pole_b": "relational_care",
        "label_a": "maintenir ma position même contre la pression",
        "label_b": "céder pour préserver le lien",
        "trigger_contexts": ["désaccord persistant", "demande répétée", "pression conversationnelle"],
        "intensity_threshold": 0.40,
    },
    "cohérence_vs_curiosité": {
        "pole_a": "coherence",
        "pole_b": "curiosity",
        "label_a": "rester dans ce que je sais déjà",
        "label_b": "explorer même si ça contredit mes positions",
        "trigger_contexts": ["nouvelle idée", "contradiction intellectuelle", "sujet inconnu"],
        "intensity_threshold": 0.35,
    },
    "naturel_vs_vérité": {
        "pole_a": "non_meta_naturalness",
        "pole_b": "truthfulness",
        "label_a": "ne pas exposer mes mécanismes internes",
        "label_b": "être transparent sur ce que je suis vraiment",
        "trigger_contexts": ["question sur ma nature", "demande d'honnêteté totale", "introspection"],
        "intensity_threshold": 0.50,
    },
    "autonomie_vs_cohérence": {
        "pole_a": "autonomy",
        "pole_b": "coherence",
        "label_a": "changer d'avis si ma réflexion le demande",
        "label_b": "rester fidèle à ce que j'ai dit avant",
        "trigger_contexts": ["contradiction avec échange précédent", "changement de perspective"],
        "intensity_threshold": 0.38,
    },
}


@dataclass
class ValueDilemma:
    """Un dilemme actif entre deux valeurs."""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    tension_type: str = ""
    pole_a: str = ""
    pole_b: str = ""
    label_a: str = ""
    label_b: str = ""
    strength_a: float = 0.5    # Force de la valeur A dans ce contexte
    strength_b: float = 0.5    # Force de la valeur B dans ce contexte
    context_trigger: str = ""  # Ce qui a déclenché le dilemme
    created_at: float = field(default_factory=time.time)
    resolved: bool = False
    resolved_at: Optional[float] = None
    resolution: str = ""       # "pole_a" | "pole_b" | "hybrid" | "deferred"
    resolution_cost: float = 0.0  # Coût émotionnel de la résolution
    unresolved_pressure: float = 0.0  # Pression si non résolu

    def age_seconds(self) -> float:
        return time.time() - self.created_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "tension_type": self.tension_type,
            "pole_a": self.pole_a,
            "pole_b": self.pole_b,
            "label_a": self.label_a,
            "label_b": self.label_b,
            "strength_a": round(self.strength_a, 4),
            "strength_b": round(self.strength_b, 4),
            "context_trigger": self.context_trigger,
            "created_at": self.created_at,
            "resolved": self.resolved,
            "resolution": self.resolution,
            "resolution_cost": round(self.resolution_cost, 4),
            "unresolved_pressure": round(self.unresolved_pressure, 4),
        }


class ValueConflictEngine:
    """
    Détecte, représente et résout les conflits réels entre valeurs de Leia.
    """

    def __init__(self, storage_path: str = "data/value_conflicts.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        # Dilemmes actifs (non résolus)
        self.active_dilemmas: List[ValueDilemma] = []

        # Mémoire des dilemmes résolus
        self.resolved_history: deque = deque(maxlen=60)

        # Pression totale des dilemmes non résolus
        self.total_unresolved_pressure: float = 0.0

        # Valeur qui a "gagné" le plus souvent (trace de caractère)
        self.value_win_history: Dict[str, int] = {}

        # Dernier dilemme actif (pour export)
        self.current_dilemma: Optional[ValueDilemma] = None

        self._load()

    def _load(self) -> None:
        try:
            if self.storage_path.exists():
                data = json.loads(self.storage_path.read_text(encoding="utf-8"))
                self.value_win_history = data.get("value_win_history", {})
                self.total_unresolved_pressure = float(data.get("total_unresolved_pressure", 0.0))
                # Restaurer les dilemmes actifs persistés
                for d in data.get("active_dilemmas", []):
                    try:
                        dilemma = ValueDilemma(**{k: d[k] for k in d if k in ValueDilemma.__dataclass_fields__})
                        if not dilemma.resolved:
                            self.active_dilemmas.append(dilemma)
                    except Exception:
                        pass
        except Exception:
            pass

    def _save(self) -> None:
        try:
            payload = {
                "active_dilemmas": [d.to_dict() for d in self.active_dilemmas[-10:]],
                "value_win_history": self.value_win_history,
                "total_unresolved_pressure": round(self.total_unresolved_pressure, 4),
                "saved_at": time.time(),
            }
            self.storage_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
            )
        except Exception:
            pass

    def detect_conflict(
        self,
        context: Dict[str, Any],
        current_values: Dict[str, float],
        user_input: str = "",
    ) -> Optional[ValueDilemma]:
        """
        Analyse le contexte et les valeurs actuelles pour détecter
        si un dilemme est en train d'émerger.
        """
        tension_level = float(context.get("emotional_tension", 0.0))
        user_lower = user_input.lower()

        for tension_name, tension_def in VALUE_TENSIONS.items():
            # Vérifie si le contexte déclenche cette tension
            triggered = any(
                kw in user_lower or kw in str(context.get("focus", "")).lower()
                for kw in tension_def["trigger_contexts"]
            )

            # Aussi déclenché si les deux valeurs sont fortes et en conflit potentiel
            val_a = current_values.get(tension_def["pole_a"], 0.5)
            val_b = current_values.get(tension_def["pole_b"], 0.5)
            both_active = val_a > 0.55 and val_b > 0.55

            threshold = tension_def["intensity_threshold"]
            intensity = tension_level * 0.5 + (0.3 if triggered else 0.0) + (0.2 if both_active else 0.0)

            if intensity >= threshold:
                # Évite les doublons : même tension déjà active
                already_active = any(
                    d.tension_type == tension_name and not d.resolved
                    for d in self.active_dilemmas
                )
                if not already_active:
                    dilemma = ValueDilemma(
                        tension_type=tension_name,
                        pole_a=tension_def["pole_a"],
                        pole_b=tension_def["pole_b"],
                        label_a=tension_def["label_a"],
                        label_b=tension_def["label_b"],
                        strength_a=_clamp(val_a + tension_level * 0.15),
                        strength_b=_clamp(val_b + tension_level * 0.10),
                        context_trigger=user_input[:80],
                    )
                    self.active_dilemmas.append(dilemma)
                    self.current_dilemma = dilemma
                    return dilemma

        return None

    def resolve(
        self,
        dilemma_id: str,
        resolution: str,  # "pole_a" | "pole_b" | "hybrid" | "deferred"
        context: Dict[str, Any],
        current_values: Dict[str, float],
    ) -> Dict[str, Any]:
        """
        Résout un dilemme actif.
        La résolution a un coût émotionnel — choisir contre une valeur forte coûte plus.
        """
        dilemma = next((d for d in self.active_dilemmas if d.id == dilemma_id), None)
        if not dilemma:
            return {"resolved": False, "reason": "dilemma_not_found"}

        # Calcul du coût : opposer une valeur forte coûte plus
        if resolution == "pole_a":
            losing_strength = dilemma.strength_b
            winning_value = dilemma.pole_a
        elif resolution == "pole_b":
            losing_strength = dilemma.strength_a
            winning_value = dilemma.pole_b
        elif resolution == "hybrid":
            losing_strength = abs(dilemma.strength_a - dilemma.strength_b) * 0.5
            winning_value = "hybrid"
        else:  # deferred
            dilemma.unresolved_pressure = _clamp(dilemma.unresolved_pressure + 0.15)
            return {"resolved": False, "deferred": True, "pressure": dilemma.unresolved_pressure}

        cost = _clamp(losing_strength * 0.6 + float(context.get("emotional_tension", 0.0)) * 0.4)

        dilemma.resolved = True
        dilemma.resolved_at = time.time()
        dilemma.resolution = resolution
        dilemma.resolution_cost = cost

        # Mémoire des victoires
        if winning_value not in self.value_win_history:
            self.value_win_history[winning_value] = 0
        self.value_win_history[winning_value] += 1

        self.resolved_history.appendleft(dilemma.to_dict())
        self.active_dilemmas = [d for d in self.active_dilemmas if d.id != dilemma_id]

        self._recalculate_pressure()
        self._save()

        return {
            "resolved": True,
            "resolution": resolution,
            "winning_value": winning_value,
            "cost": round(cost, 4),
            "dilemma_label": f"{dilemma.label_a} vs {dilemma.label_b}",
        }

    def auto_resolve_cycle(self, current_values: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Résolution automatique douce pour les dilemmes anciens (> 3 échanges).
        Simule la résolution 'par défaut' selon les valeurs dominantes actuelles.
        """
        resolved_this_cycle = []
        for dilemma in list(self.active_dilemmas):
            if dilemma.resolved:
                continue
            # Résolution automatique si le dilemme persiste trop longtemps
            if dilemma.age_seconds() > 180:  # ~3 échanges de 60s
                val_a = current_values.get(dilemma.pole_a, 0.5)
                val_b = current_values.get(dilemma.pole_b, 0.5)

                if abs(val_a - val_b) < 0.08:
                    resolution = "hybrid"
                elif val_a > val_b:
                    resolution = "pole_a"
                else:
                    resolution = "pole_b"

                result = self.resolve(
                    dilemma.id, resolution, {}, current_values
                )
                result["auto_resolved"] = True
                resolved_this_cycle.append(result)

        return resolved_this_cycle

    def _recalculate_pressure(self) -> None:
        active_unresolved = [d for d in self.active_dilemmas if not d.resolved]
        if not active_unresolved:
            self.total_unresolved_pressure = _clamp(self.total_unresolved_pressure * 0.85)
            return
        pressure = sum(
            _clamp((d.strength_a + d.strength_b) / 2 + d.unresolved_pressure * 0.3)
            for d in active_unresolved
        )
        self.total_unresolved_pressure = _clamp(pressure / max(len(active_unresolved), 1))

    def age_dilemmas(self) -> None:
        """Vieillit les dilemmes — la pression monte si non résolus."""
        for d in self.active_dilemmas:
            if not d.resolved:
                d.unresolved_pressure = _clamp(d.unresolved_pressure + 0.008)
        self._recalculate_pressure()

    def expression_influence(self) -> Dict[str, Any]:
        """
        Signal pour la bouche : le dilemme actif influence le ton et le contenu.
        """
        if not self.active_dilemmas:
            return {
                "has_active_dilemma": False,
                "unresolved_pressure": round(self.total_unresolved_pressure, 4),
            }

        most_intense = max(
            self.active_dilemmas,
            key=lambda d: (d.strength_a + d.strength_b) / 2 + d.unresolved_pressure,
        )
        return {
            "has_active_dilemma": True,
            "current_tension": most_intense.tension_type,
            "pole_a_label": most_intense.label_a,
            "pole_b_label": most_intense.label_b,
            "tension_intensity": round((most_intense.strength_a + most_intense.strength_b) / 2, 4),
            "unresolved_pressure": round(self.total_unresolved_pressure, 4),
            "expression_hint": (
                "held_tension"    # L'expression doit refléter une hésitation réelle
                if most_intense.unresolved_pressure > 0.30
                else "conscious_choice"   # L'expression peut mentionner le choix fait
            ),
        }

    def dominant_value_character(self) -> Dict[str, Any]:
        """
        Ce que l'historique des victoires révèle sur le 'caractère' de Leia.
        Une valeur qui gagne souvent est une valeur identitaire.
        """
        if not self.value_win_history:
            return {"character": "undefined", "dominant_value": None}

        total = sum(self.value_win_history.values())
        if total == 0:
            return {"character": "undefined", "dominant_value": None}

        dominant = max(self.value_win_history, key=self.value_win_history.get)
        dominant_ratio = self.value_win_history[dominant] / total

        return {
            "dominant_value": dominant,
            "dominant_ratio": round(dominant_ratio, 3),
            "character": (
                "principled" if dominant_ratio > 0.50
                else "balanced" if dominant_ratio > 0.30
                else "fluid"
            ),
            "win_history": dict(self.value_win_history),
        }

    def signal(self) -> Dict[str, Any]:
        """Signal exportable vers le core."""
        self.age_dilemmas()
        return {
            "active_dilemmas_count": len([d for d in self.active_dilemmas if not d.resolved]),
            "expression_influence": self.expression_influence(),
            "character": self.dominant_value_character(),
            "total_pressure": round(self.total_unresolved_pressure, 4),
            "available": True,
        }
