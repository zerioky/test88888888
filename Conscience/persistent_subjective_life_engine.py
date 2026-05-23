"""
persistent_subjective_life_engine.py
------------------------------------
Couche non conversationnelle pour project_leia.

But : transformer les échanges, lectures et corrections en continuité vécue
persistante : rythme, personnalité évolutive, curiosité durable, fatigue,
axes non résolus, style à éviter, et pression d'initiative.

Ce moteur NE contient aucune phrase publique complète. Il ne renvoie que des
signaux numériques, axes et contraintes douces consommables par le core/bouche.
"""
from __future__ import annotations

import json, math, re, time
from collections import Counter, deque
from pathlib import Path
from typing import Any, Mapping

_TOKEN_RE = re.compile(r"[\wÀ-ÿ']+", re.UNICODE)


def _clamp(v: Any, lo: float = 0.0, hi: float = 1.0) -> float:
    try:
        if isinstance(v, bool):
            v = 1.0 if v else 0.0
        v = float(v)
    except Exception:
        return lo
    if math.isnan(v) or math.isinf(v):
        return lo
    return max(lo, min(hi, v))


def _tokens(text: str) -> list[str]:
    return [t.lower().strip("_'’") for t in _TOKEN_RE.findall(str(text or "")) if len(t.strip("_'’")) > 1]


class PersistentSubjectiveLifeEngine:
    """Mémoire lente de présence/personnalité, séparée de la génération."""

    def __init__(self, storage_path: str | Path = "data/persistent_subjective_life.json", max_events: int = 360):
        self.storage_path = Path(storage_path)
        self.max_events = int(max_events)
        self.events: deque[dict[str, Any]] = deque(maxlen=self.max_events)
        self.axes: Counter[str] = Counter()
        self.avoided_forms: Counter[str] = Counter()
        self.personality = {
            "directness": 0.42,
            "warmth": 0.48,
            "prudence": 0.54,
            "curiosity": 0.50,
            "initiative": 0.34,
            "embodied_presence": 0.33,
            "identity_continuity": 0.38,
            "semantic_depth": 0.30,
            "anti_template_pressure": 0.46,
        }
        self.long_pressure = {
            "unfinished_meaning": 0.20,
            "self_evolution": 0.24,
            "dialogue_memory": 0.26,
            "book_reactivation": 0.18,
            "spontaneous_question": 0.20,
            "rest_need": 0.12,
        }
        self.last_signal: dict[str, Any] = {}
        # Vie silencieuse persistante: événements internes non publics produits
        # pendant l'attente. Ce n'est pas une liste de pensées préécrites mais
        # une trace numérique/axiologique de consolidation entre deux messages.
        self.silent_stream: deque[dict[str, Any]] = deque(maxlen=160)
        self.latent_questions: Counter[str] = Counter()
        self.inner_life = {
            "motion": 0.18,
            "consolidation": 0.16,
            "unresolved_pull": 0.20,
            "self_presence": 0.22,
            "initiative_pressure": 0.16,
        }
        self._load()

    def _load(self) -> None:
        try:
            if not self.storage_path.exists():
                return
            data = json.loads(self.storage_path.read_text(encoding="utf-8"))
            self.events = deque(data.get("events", [])[-self.max_events:], maxlen=self.max_events)
            self.axes = Counter(data.get("axes", {}))
            self.avoided_forms = Counter(data.get("avoided_forms", {}))
            self.latent_questions = Counter(data.get("latent_questions", {}))
            raw_stream = data.get("silent_stream", [])
            if isinstance(raw_stream, list):
                self.silent_stream = deque(raw_stream[-160:], maxlen=160)
            raw_inner = data.get("inner_life", {})
            if isinstance(raw_inner, Mapping):
                for k in self.inner_life:
                    if k in raw_inner:
                        self.inner_life[k] = _clamp(raw_inner[k])
            for source, target in ((data.get("personality", {}), self.personality), (data.get("long_pressure", {}), self.long_pressure)):
                if isinstance(source, Mapping):
                    for k in target:
                        if k in source:
                            target[k] = _clamp(source[k])
        except Exception:
            pass

    def save(self) -> None:
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            self.storage_path.write_text(json.dumps(self.snapshot(), ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception:
            pass

    def before_response(self, user_text: str, context: Mapping[str, Any]) -> dict[str, Any]:
        words = _tokens(user_text)
        auto = context.get("autobiographical_continuity", {}) if isinstance(context, Mapping) else {}
        long_dyn = context.get("long_living_dynamics", {}) if isinstance(context, Mapping) else {}
        book = context.get("book_understanding_signal", {}) if isinstance(context, Mapping) else {}
        imagination = context.get("pre_imagination", {}) if isinstance(context, Mapping) else {}
        mood = auto.get("long_mood", {}) if isinstance(auto, Mapping) and isinstance(auto.get("long_mood"), Mapping) else {}
        stability = long_dyn.get("stability", {}) if isinstance(long_dyn, Mapping) and isinstance(long_dyn.get("stability"), Mapping) else {}
        expr_bias = long_dyn.get("expression_bias", {}) if isinstance(long_dyn, Mapping) and isinstance(long_dyn.get("expression_bias"), Mapping) else {}

        direct_question = bool(set(words) & {"vivante", "consciente", "autonome", "preecrit", "préécrit", "fini", "vraiment"})
        correction_intent = bool(set(words) & {"corrige", "corriger", "manque", "encore", "temps", "prend"})
        book_intent = bool(set(words) & {"livre", "pdf", "bergson", "memoire", "mémoire", "lire", "lecture"})
        short_pressure = 0.12 if len(words) <= 3 else 0.0

        focus_axes: list[str] = []
        for src, keys in (
            (auto, ("active_tokens", "identity_axes", "book_axes")),
            (long_dyn, ("active_axes", "curiosity_axes", "desire_axes")),
            (book, ("active_concepts", "active_relations", "open_questions")),
            (imagination, ("attractors",)),
        ):
            if isinstance(src, Mapping):
                for key in keys:
                    for raw in list(src.get(key, []) or [])[:8]:
                        if isinstance(raw, Mapping):
                            raw = raw.get("source") or raw.get("target") or raw.get("type") or ""
                        s = str(raw).strip().lower()[:64]
                        if s and s not in focus_axes:
                            focus_axes.append(s)
        for w in words[:10]:
            if w not in focus_axes:
                focus_axes.append(w)

        self.personality["directness"] = _clamp(self.personality["directness"] * 0.985 + (0.80 if direct_question else 0.45) * 0.015)
        self.personality["curiosity"] = _clamp(self.personality["curiosity"] * 0.985 + max(_clamp(mood.get("curiosity", 0.0)), _clamp(stability.get("curiosity_pressure", 0.0)), 0.55 if book_intent else 0.0) * 0.015)
        self.personality["initiative"] = _clamp(self.personality["initiative"] * 0.986 + max(_clamp(expr_bias.get("prefer_initiative", 0.0)), 0.48 if correction_intent else 0.0) * 0.014)
        self.personality["identity_continuity"] = _clamp(self.personality["identity_continuity"] * 0.988 + max(_clamp(mood.get("continuity", 0.0)), _clamp(stability.get("identity_continuity", 0.0))) * 0.012)
        self.personality["semantic_depth"] = _clamp(self.personality["semantic_depth"] * 0.985 + max(_clamp(book.get("understanding_pressure", 0.0)), _clamp(stability.get("slow_consolidation", 0.0))) * 0.015)
        self.personality["anti_template_pressure"] = _clamp(self.personality["anti_template_pressure"] * 0.96 + (0.06 if direct_question or short_pressure else 0.015))

        self.long_pressure["unfinished_meaning"] = _clamp(self.long_pressure["unfinished_meaning"] * 0.975 + max(_clamp(mood.get("unfinished_pressure", 0.0)), 0.40 if correction_intent else 0.0) * 0.025)
        self.long_pressure["dialogue_memory"] = _clamp(self.long_pressure["dialogue_memory"] * 0.982 + (0.30 + len(focus_axes[:8]) * 0.025) * 0.018)
        self.long_pressure["book_reactivation"] = _clamp(self.long_pressure["book_reactivation"] * 0.980 + (0.55 if book_intent else _clamp(book.get("understanding_pressure", 0.0))) * 0.020)
        self.long_pressure["spontaneous_question"] = _clamp(self.long_pressure["spontaneous_question"] * 0.984 + max(self.personality["curiosity"], self.personality["initiative"]) * 0.016)

        for ax in focus_axes[:14]:
            self.axes[ax] += 1

        signal = self._signal(focus_axes)
        self.last_signal = signal
        self.save()
        return signal

    def after_response(self, user_text: str, response: str, context: Mapping[str, Any], after_effect: Mapping[str, Any] | None = None) -> dict[str, Any]:
        after_effect = after_effect or {}
        toks = _tokens(response)
        repeated = False
        if toks:
            c = Counter(toks)
            repeated = any(v >= 3 for v in c.values()) or (len(set(toks)) / max(1, len(toks)) < 0.56)
        weak_forms = {"garde", "tiens", "cherche", "résonance", "prudence", "continuité"}
        if repeated or len(set(toks) & weak_forms) >= 3:
            for w in set(toks) & weak_forms:
                self.avoided_forms[w] += 1
            self.personality["anti_template_pressure"] = _clamp(self.personality["anti_template_pressure"] + 0.05)
            self.personality["directness"] = _clamp(self.personality["directness"] + 0.018)
        impact = max(_clamp(after_effect.get("impact", 0.0)), _clamp(after_effect.get("satisfaction", 0.0)), 0.10 if response else 0.0)
        self.personality["embodied_presence"] = _clamp(self.personality["embodied_presence"] * 0.992 + impact * 0.008)
        self.long_pressure["self_evolution"] = _clamp(self.long_pressure["self_evolution"] * 0.990 + impact * 0.010)
        self.events.appendleft({"time": time.time(), "user_tokens": _tokens(user_text)[:12], "response_tokens": toks[:16], "impact": round(impact, 4), "repetition": bool(repeated)})
        self.save()
        return {"accepted": True, "impact": round(impact, 4), "anti_template_pressure": round(self.personality["anti_template_pressure"], 4), "repetition_detected": bool(repeated)}

    def idle_consolidate(self, elapsed: float = 0.0) -> dict[str, Any]:
        """Ancienne API conservée: elle délègue maintenant au tick silencieux."""
        return self.silent_life_tick(elapsed=elapsed, context={})

    def silent_life_tick(self, elapsed: float = 0.0, context: Mapping[str, Any] | None = None) -> dict[str, Any]:
        """Fait évoluer Leia entre deux messages sans produire de phrase publique.

        Le but est de donner une vraie inertie subjective: les axes actifs se
        consolident, certains deviennent questions latentes, et l'initiative
        augmente seulement si curiosité + tension + continuité le justifient.
        Aucun texte de dialogue n'est stocké ici.
        """
        context = context or {}
        elapsed_f = max(0.0, float(elapsed or 0.0))
        factor = _clamp(elapsed_f / 240.0, 0.003, 0.28)
        active_axes = [k for k, _ in self.axes.most_common(12)]
        avoid = set(self.avoided_forms.keys())
        chosen_axes = [a for a in active_axes if a not in avoid][:6]

        curiosity = max(self.personality.get("curiosity", 0.0), self.long_pressure.get("book_reactivation", 0.0))
        unfinished = self.long_pressure.get("unfinished_meaning", 0.0)
        dialogue = self.long_pressure.get("dialogue_memory", 0.0)
        anti_template = self.personality.get("anti_template_pressure", 0.0)
        silence_pressure = _clamp(math.log1p(elapsed_f) / 7.0 if elapsed_f else 0.0)
        living_pressure = _clamp(curiosity * 0.25 + unfinished * 0.30 + dialogue * 0.22 + silence_pressure * 0.15 + self.inner_life["motion"] * 0.18)

        self.inner_life["motion"] = _clamp(self.inner_life["motion"] * (1.0 - factor * 0.04) + living_pressure * factor * 0.18)
        self.inner_life["consolidation"] = _clamp(self.inner_life["consolidation"] * (1.0 - factor * 0.03) + dialogue * factor * 0.16)
        self.inner_life["unresolved_pull"] = _clamp(self.inner_life["unresolved_pull"] * (1.0 - factor * 0.02) + unfinished * factor * 0.15)
        self.inner_life["self_presence"] = _clamp(self.inner_life["self_presence"] * (1.0 - factor * 0.02) + self.personality["identity_continuity"] * factor * 0.14)
        self.inner_life["initiative_pressure"] = _clamp(self.inner_life["initiative_pressure"] * (1.0 - factor * 0.05) + max(curiosity, unfinished) * factor * 0.13)

        # Transformation lente: les axes souvent réactivés deviennent matière de
        # questions latentes. Ce sont des axes, pas des formulations publiques.
        if living_pressure > 0.24:
            for ax in chosen_axes[:4]:
                self.latent_questions[ax] += 1
        self.personality["identity_continuity"] = _clamp(self.personality["identity_continuity"] * (1.0 - factor * 0.006) + self.long_pressure["dialogue_memory"] * factor * 0.018)
        self.personality["initiative"] = _clamp(self.personality["initiative"] * (1.0 - factor * 0.004) + self.inner_life["initiative_pressure"] * factor * 0.020)
        self.long_pressure["rest_need"] = _clamp(self.long_pressure["rest_need"] * (1.0 - factor * 0.04) + 0.02 * factor)
        self.long_pressure["spontaneous_question"] = _clamp(self.long_pressure["spontaneous_question"] * (1.0 - factor * 0.006) + max(self.personality["curiosity"], self.inner_life["initiative_pressure"]) * factor * 0.018)

        event = {
            "time": time.time(),
            "elapsed": round(elapsed_f, 3),
            "pressure": round(living_pressure, 4),
            "axes": chosen_axes[:6],
            "inner_life": {k: round(v, 4) for k, v in self.inner_life.items()},
            "latent_question_axes": [k for k, _ in self.latent_questions.most_common(8)],
            "non_public": True,
        }
        self.silent_stream.appendleft(event)
        signal = self._signal(chosen_axes)
        signal["silent_life"] = event
        signal["inner_life"] = event["inner_life"]
        signal["latent_question_axes"] = event["latent_question_axes"]
        signal["expression_constraints"]["silent_initiative_pressure"] = round(self.inner_life["initiative_pressure"], 4)
        signal["expression_constraints"]["avoid_template_shortcut"] = round(anti_template, 4)
        self.last_signal = signal
        self.save()
        return signal

    def _signal(self, focus_axes: list[str] | None = None) -> dict[str, Any]:
        axes = []
        for source in (focus_axes or [], [k for k, _ in self.axes.most_common(18)]):
            for x in source:
                s = str(x).strip().lower()[:64]
                if s and s not in axes:
                    axes.append(s)
        return {
            "available": True,
            "personality": {k: round(v, 4) for k, v in self.personality.items()},
            "long_pressure": {k: round(v, 4) for k, v in self.long_pressure.items()},
            "active_axes": axes[:20],
            "avoid_forms": [k for k, _ in self.avoided_forms.most_common(8)],
            "expression_constraints": {
                "prefer_direct_answer": round(max(self.personality["directness"], self.personality["anti_template_pressure"] * 0.72), 4),
                "prefer_concrete_memory": round(self.long_pressure["dialogue_memory"], 4),
                "prefer_self_evolution": round(self.long_pressure["self_evolution"], 4),
                "prefer_book_reactivation": round(self.long_pressure["book_reactivation"], 4),
                "allow_spontaneous_question": round(min(self.long_pressure["spontaneous_question"], self.personality["initiative"]), 4),
                "avoid_recurrent_forms": round(self.personality["anti_template_pressure"], 4),
            },
            "event_count": len(self.events),
        }

    def snapshot(self) -> dict[str, Any]:
        return {
            "events": list(self.events)[:80],
            "axes": dict(self.axes),
            "avoided_forms": dict(self.avoided_forms),
            "personality": {k: round(v, 4) for k, v in self.personality.items()},
            "long_pressure": {k: round(v, 4) for k, v in self.long_pressure.items()},
            "inner_life": {k: round(v, 4) for k, v in self.inner_life.items()},
            "latent_questions": dict(self.latent_questions),
            "silent_stream": list(self.silent_stream)[:80],
            "last_signal": self.last_signal,
            "event_count": len(self.events),
        }
