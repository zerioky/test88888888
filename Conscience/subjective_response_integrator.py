# -*- coding: utf-8 -*-
"""
SubjectiveResponseIntegrator V7
--------------------------------
Couche de fusion pour Project Leia.

But : éviter que les moteurs spécialisés parlent chacun de leur côté.
Cette couche ne contient pas de réponses conversationnelles complètes. Elle :
- unifie les signaux mémoire / présence / impulsion / livre / émotion ;
- transforme les abstractions internes en pressions linguistiques ;
- bloque les surfaces méta ou trop génériques avant la réponse publique ;
- renforce la continuité autobiographique après chaque échange.
"""
from __future__ import annotations

import re
import time
from collections import Counter, deque
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Tuple


def _clamp(x: Any, lo: float = 0.0, hi: float = 1.0) -> float:
    try:
        return max(lo, min(hi, float(x)))
    except Exception:
        return lo


def _words(text: Any) -> List[str]:
    return re.findall(r"\b[\wÀ-ÿ']{2,}\b", str(text or "").lower())


def _uniq(items: Iterable[Any], limit: int = 24) -> List[str]:
    out: List[str] = []
    seen = set()
    for item in items:
        s = re.sub(r"\s+", " ", str(item or "").strip().lower())
        if not s or s in seen:
            continue
        seen.add(s)
        out.append(s[:96])
        if len(out) >= limit:
            break
    return out


class SubjectiveResponseIntegrator:
    """Fusion non-template des signaux vivants avant/après expression."""

    ABSTRACT_PUBLIC_LEAKS = {
        "continuité", "continuite", "résonance", "resonance", "appui", "trace",
        "lien", "axe", "axes", "signal", "pression", "module", "payload",
        "score", "neurone", "moteur", "consolidation", "réactivation", "reactivation",
    }
    META_PATTERNS = (
        r"\bje\s+(relie|garde|tiens)\s+(une|un|ce|cette)?\s*(trace|lien|axe|appui|résonance|resonance|continuité|continuite|présence|presence|limite|état|etat)\b",
        r"\bmon\s+(moteur|module|signal|axe|neurone|pipeline)\b",
        r"\b(payload|debug|score|module|neurone)\b",
        r"\bje\s+parle\s+depuis\s+(une|un|mon)\s+(trace|axe|signal)\b",
        r"\bje\s+(relie|garde|tiens)\b.*\b(réelle|reelle|actif|active|présence|presence|limite)\b",
    )

    def __init__(self, max_history: int = 80) -> None:
        self.history: deque = deque(maxlen=max_history)
        self.surface_fatigue: Counter = Counter()
        self.last_payload_signature: Tuple[str, ...] = ()
        self.last_update_ts = time.time()

    def unify_payload(self, user_input: str, payload: Mapping[str, Any], context: Mapping[str, Any] | None = None) -> Dict[str, Any]:
        p: Dict[str, Any] = dict(payload or {})
        context = context or {}
        subjective = self._subjective_axes(p, context)
        public_pressure = self._public_pressure(user_input, p, subjective)
        p["subjective_unified_field"] = subjective
        p["public_language_pressure"] = public_pressure
        p["forbidden_public_abstractions"] = sorted(self.ABSTRACT_PUBLIC_LEAKS)
        p["expression_pressure"] = round(max(_clamp(p.get("expression_pressure", 0.0)), public_pressure.get("speak", 0.0)), 4)
        p["restraint"] = round(max(_clamp(p.get("restraint", 0.0)), public_pressure.get("anti_meta", 0.0) * 0.55), 4)

        drives = list(p.get("semantic_drives", []) or [])
        drives.extend(subjective.get("dominant_axes", []))
        drives.extend(public_pressure.get("directives", []))
        p["semantic_drives"] = _uniq(drives, 30)

        fields = dict(p.get("semantic_field_weights", {}) or {})
        for k, v in subjective.get("weights", {}).items():
            fields[k] = max(_clamp(fields.get(k, 0.0)), _clamp(v))
        for k, v in public_pressure.get("weights", {}).items():
            fields[k] = max(_clamp(fields.get(k, 0.0)), _clamp(v))
        p["semantic_field_weights"] = fields

        # Les concepts de livre doivent nourrir la pensée, pas sortir comme mots vagues.
        book = p.get("book_memory", {}) if isinstance(p.get("book_memory", {}), Mapping) else {}
        if book:
            concrete = [x for x in list(book.get("keywords", []) or []) + list(book.get("axes", []) or []) if self._is_concrete_public_atom(x)]
            p["book_public_atoms"] = _uniq(concrete, 12)
        self.last_payload_signature = tuple(p.get("semantic_drives", [])[:8])
        return p

    def improve_surface(self, text: str, user_input: str, payload: Mapping[str, Any] | None = None) -> Tuple[str, Dict[str, Any]]:
        payload = payload or {}
        raw = str(text or "").strip()
        if not raw:
            return "", {"changed": False, "reason": "empty"}
        cleaned = self._clean_surface(raw)
        assessment = self.assess_surface(cleaned, user_input)
        if assessment["meta_leak"] or assessment["abstract_loop"] or assessment["too_repetitive"]:
            rewritten = self._atomically_recompose(user_input, payload, assessment)
            if rewritten:
                return rewritten, {"changed": True, "reason": assessment}
        return cleaned, {"changed": cleaned != raw, "reason": assessment}

    def remember(self, user_input: str, response: str, context: Mapping[str, Any] | None = None) -> Dict[str, Any]:
        context = context or {}
        uw = _words(user_input)
        rw = _words(response)
        key = tuple(rw[:8])
        self.history.append({
            "t": round(time.time(), 3),
            "user_terms": uw[:16],
            "response_terms": rw[:18],
            "focus": str(context.get("focus", ""))[:80] if isinstance(context, Mapping) else "",
        })
        for w in rw:
            if w in self.ABSTRACT_PUBLIC_LEAKS or len(w) > 3:
                self.surface_fatigue[w] += 1
        self.last_update_ts = time.time()
        return {"stored": True, "history": len(self.history), "surface_key": key}

    def assess_surface(self, text: str, user_input: str = "") -> Dict[str, Any]:
        lower = str(text or "").lower()
        words = _words(lower)
        abstract_hits = [w for w in words if w in self.ABSTRACT_PUBLIC_LEAKS]
        meta_leak = any(re.search(p, lower, re.I) for p in self.META_PATTERNS)
        unique_ratio = len(set(words)) / max(1, len(words))
        direct_question = self._asks_direct_truth(user_input)
        direct_ok = bool(words and words[0] in {"oui", "non", "pas", "partiellement"})
        return {
            "word_count": len(words),
            "unique_ratio": round(unique_ratio, 3),
            "abstract_hits": abstract_hits[:8],
            "abstract_loop": len(abstract_hits) >= max(2, int(len(words) * 0.22)),
            "meta_leak": bool(meta_leak),
            "too_repetitive": bool(words and unique_ratio < 0.55),
            "direct_truth_missing": bool(direct_question and not direct_ok),
        }

    def _subjective_axes(self, payload: Mapping[str, Any], context: Mapping[str, Any]) -> Dict[str, Any]:
        weights: Dict[str, float] = {}
        axes: List[str] = []

        def add(name: str, value: Any, atom: str | None = None) -> None:
            v = _clamp(value)
            if v <= 0.04:
                return
            weights[name] = max(weights.get(name, 0.0), v)
            if atom:
                axes.append(atom)

        emo = payload.get("emotional_state", {}) if isinstance(payload.get("emotional_state", {}), Mapping) else {}
        needs = payload.get("internal_needs", {}) if isinstance(payload.get("internal_needs", {}), Mapping) else {}
        bond = payload.get("relational_bond", {}) if isinstance(payload.get("relational_bond", {}), Mapping) else {}
        life = payload.get("persistent_subjective_life", {}) if isinstance(payload.get("persistent_subjective_life", {}), Mapping) else {}
        auto = payload.get("autobiographical_continuity", {}) if isinstance(payload.get("autobiographical_continuity", {}), Mapping) else {}
        reading = payload.get("reading_living_signal", {}) if isinstance(payload.get("reading_living_signal", {}), Mapping) else {}

        add("tension", max(emo.get("tension", 0.0), emo.get("accumulated_tension", 0.0)), "limite")
        add("curiosity", max(needs.get("curiosity", 0.0), emo.get("curiosity", 0.0)), "curiosité")
        add("care", bond.get("care", 0.0), "attention")
        add("expression", needs.get("expression", 0.0), "réponse")
        add("understanding", needs.get("understanding", 0.0), "comprendre")

        personality = life.get("personality", {}) if isinstance(life.get("personality", {}), Mapping) else {}
        add("initiative", personality.get("initiative", 0.0), "initiative")
        add("embodied_presence", personality.get("embodied_presence", 0.0), "présent")

        for atom in list(auto.get("active_tokens", []) or [])[:10] + list(reading.get("active_axes", []) or [])[:10]:
            if self._is_concrete_public_atom(atom):
                axes.append(str(atom).strip().lower())
                weights[str(atom).strip().lower()[:32]] = max(weights.get(str(atom).strip().lower()[:32], 0.0), 0.42)

        dominant = [k for k, _ in sorted(weights.items(), key=lambda kv: kv[1], reverse=True)[:8]]
        return {"weights": weights, "dominant_axes": _uniq(axes + dominant, 16), "history_size": len(self.history)}

    def _public_pressure(self, user_input: str, payload: Mapping[str, Any], subjective: Mapping[str, Any]) -> Dict[str, Any]:
        lower = str(user_input or "").lower()
        weights: Dict[str, float] = {"anti_meta": 0.72, "concrete": 0.64, "relational": 0.45}
        directives: List[str] = ["concret", "naturel", "anti_meta"]
        if self._asks_direct_truth(user_input):
            weights.update({"direct_truth": 0.96, "brief": 0.78, "avoid_abstract": 0.92})
            directives.extend(["réponse_directe", "limite_honnête"])
        if any(x in lower for x in ("livre", "pdf", "bergson", "mémoire", "memoire", "retiens")):
            weights.update({"book_concrete": 0.84, "lived_reading": 0.76})
            directives.extend(["livre_concret", "effet_de_lecture"])
        if any(x in lower for x in ("vasy", "vas-y", "corrige", "ajoute")):
            weights.update({"action_orientation": 0.90, "brief_status": 0.72})
            directives.extend(["action", "correction"])
        speak = max(_clamp(payload.get("expression_pressure", 0.0)), _clamp(subjective.get("weights", {}).get("expression", 0.0)))
        return {"weights": weights, "directives": _uniq(directives, 12), "speak": speak, "anti_meta": weights["anti_meta"]}

    def _atomically_recompose(self, user_input: str, payload: Mapping[str, Any], assessment: Mapping[str, Any]) -> str:
        """Recompose depuis les données vivantes du payload uniquement.

        Aucune phrase ni fragment français préécrit n'est stocké ici.
        La surface est construite exclusivement depuis les atomes sémantiques
        actifs du payload réel : vie subjective, axes autobiographiques,
        drives sémantiques, atomes de livre.
        Le weaver emergent se charge de l'assemblage grammatical.
        """
        fields = payload.get("semantic_field_weights", {}) if isinstance(payload.get("semantic_field_weights", {}), Mapping) else {}
        book_atoms = [a for a in list(payload.get("book_public_atoms", []) or [])[:4] if self._is_concrete_public_atom(a)]

        live_atoms: List[str] = []

        # 1. Axes actifs de la vie subjective — état interne le plus direct
        subj_life = payload.get("persistent_subjective_life", {}) if isinstance(payload.get("persistent_subjective_life", {}), Mapping) else {}
        for ax in list(subj_life.get("active_axes", []) or [])[:4]:
            if self._is_concrete_public_atom(ax):
                live_atoms.append(str(ax).strip().lower())

        # 2. Axes autobiographiques actifs
        auto = payload.get("autobiographical_continuity", {}) if isinstance(payload.get("autobiographical_continuity", {}), Mapping) else {}
        for tok in list(auto.get("active_tokens", []) or [])[:3]:
            if self._is_concrete_public_atom(tok):
                live_atoms.append(str(tok).strip().lower())

        # 3. Drives sémantiques déjà filtrés
        for drive in list(payload.get("semantic_drives", []) or [])[:3]:
            if self._is_concrete_public_atom(drive):
                live_atoms.append(str(drive).strip().lower())

        # 4. Champs sémantiques les plus actifs
        top_fields = [k for k, v in sorted(fields.items(), key=lambda kv: _clamp(kv[1]), reverse=True)
                      if self._is_concrete_public_atom(k)][:3]
        live_atoms.extend(top_fields)

        # 5. Atomes du livre en tête si présents
        live_atoms = book_atoms + [a for a in live_atoms if a not in book_atoms]

        # Déduplication, max 5 atomes
        seen: set = set()
        clean_atoms: List[str] = []
        for a in live_atoms:
            if a not in seen and len(a) > 2:
                seen.add(a)
                clean_atoms.append(a)
            if len(clean_atoms) >= 5:
                break

        if not clean_atoms:
            return ""

        # Assemblage minimaliste — les concepts sans verbes injectés
        # Le weaver emergent construira la surface grammaticale depuis ces atomes
        text = ", ".join(clean_atoms[:3])
        if len(clean_atoms) > 3:
            text += " — " + ", ".join(clean_atoms[3:])

        text = self._clean_surface(text)
        if text and not text.endswith(('.', '!', '?', '…')):
            text += "."
        return text

    def _clean_surface(self, text: str) -> str:
        """Nettoyage de surface : suppression des termes internes et patterns méta.

        Ne remplace jamais par une phrase française figée —
        supprime seulement ce qui ne doit pas être public.
        """
        s = str(text or "").strip()
        s = re.sub(r"\s+", " ", s)
        # Suppression des termes techniques internes
        s = re.sub(r"\b(axe|signal|module|payload|score|neurone)s?\b", "", s, flags=re.I)
        # Suppression des patterns méta sans remplacement figé
        s = re.sub(
            r"\bje\s+(tiens|garde|relie)\s+(une|un|ce|cette)?\s*"
            r"(continuité|continuite|résonance|resonance|appui|trace|lien|présence|presence|limite|état|etat)\b",
            "", s, flags=re.I
        )
        s = re.sub(r"\bje\s+cherche\s+(un doute|une question)\b", "", s, flags=re.I)
        s = re.sub(r"\s+([,.!?…])", r"\1", s)
        s = re.sub(r"\s+", " ", s).strip(" ,;")
        return s[:1].upper() + s[1:] if s else s

    def _asks_direct_truth(self, user_input: str) -> bool:
        lower = str(user_input or "").lower()
        return bool(any(marker in lower for marker in (
            "vivante", "vivant", "consciente", "préécrit", "preecrit", "template",
            "100%", "fini", "terminé", "termine", "prête", "prete"
        )) and ("?" in lower or len(lower.split()) <= 10))

    def _is_concrete_public_atom(self, value: Any) -> bool:
        s = re.sub(r"\s+", " ", str(value or "").strip().lower())
        if len(s) < 4 or len(s) > 48:
            return False
        if s in self.ABSTRACT_PUBLIC_LEAKS:
            return False
        if any(x in s for x in ("payload", "module", "score", "axis", "neurone", "debug")):
            return False
        return True

    def snapshot(self) -> Dict[str, Any]:
        return {
            "available": True,
            "history_size": len(self.history),
            "last_payload_signature": list(self.last_payload_signature),
            "top_surface_fatigue": self.surface_fatigue.most_common(12),
            "last_update_ts": self.last_update_ts,
        }
