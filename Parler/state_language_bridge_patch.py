"""
state_language_bridge_patch.py
-------------------------------
Patch pour enrichir le payload d'expression de Leia avec les concepts
réellement lus et mémorisés depuis les livres PDF.

Le problème : emergent_french_weaver cherche les concepts du livre dans
book_memory, book_understanding_signal, last_book_synthesis — mais leia_living_core
ne les injecte pas toujours dans le payload final envoyé au weaver.

Ce patch ajoute une méthode enrich_payload() qui complète le payload
avec toutes les données de livre disponibles dans le living_state.

Usage dans leia_living_core.py :
    from state_language_bridge_patch import enrich_payload_with_book
    payload = enrich_payload_with_book(payload, self.living_state)
"""
from __future__ import annotations
from typing import Any, Dict, Mapping


def enrich_payload_with_book(
    payload: Dict[str, Any],
    living_state: Mapping[str, Any],
) -> Dict[str, Any]:
    """
    Enrichit le payload d'expression avec les données de livre du living_state.
    À appeler juste avant de passer le payload au weaver/generator.
    """
    if not isinstance(living_state, Mapping):
        return payload

    # ── 1. Synthèse conceptuelle du dernier livre lu ──────────────────────────
    last_synth = living_state.get("last_book_synthesis")
    if isinstance(last_synth, Mapping) and last_synth:
        payload.setdefault("last_book_synthesis", last_synth)
        payload.setdefault("conceptual_synthesis", last_synth)

    # ── 2. Compréhension profonde du livre (axes, tensions, relations) ─────────
    book_understanding = living_state.get("book_understanding")
    if isinstance(book_understanding, Mapping) and book_understanding:
        payload.setdefault("book_understanding_signal", book_understanding)
        payload.setdefault("book_memory", book_understanding)

    # ── 3. Signal de lecture vivante (concepts actifs) ─────────────────────────
    reading_signal = living_state.get("reading_living_reflection") or \
                     living_state.get("reading_living_consolidation")
    if isinstance(reading_signal, Mapping) and reading_signal:
        payload.setdefault("reading_living_signal", reading_signal)

    # ── 4. Livres lus (liste complète) ────────────────────────────────────────
    learned_books = living_state.get("learned_books", [])
    if isinstance(learned_books, list) and learned_books:
        latest = learned_books[-1]
        if isinstance(latest, Mapping):
            # Synthèse du dernier livre
            synth = latest.get("conceptual_synthesis", {})
            if isinstance(synth, Mapping) and synth:
                payload.setdefault("last_book_synthesis", synth)
                payload.setdefault("conceptual_synthesis", synth)
            # Axes et concepts extraits
            book_und = latest.get("book_understanding", {})
            if isinstance(book_und, Mapping) and book_und:
                payload.setdefault("book_understanding_signal", book_und)
                payload.setdefault("book_memory", book_und)

    # ── 5. Impregnation lexicale (mots chargés par le livre) ──────────────────
    lexical = living_state.get("lexical_impregnation")
    if isinstance(lexical, Mapping) and lexical.get("available"):
        payload.setdefault("lexical_impregnation_signal", lexical)

    # ── 6. Tensions non résolues (résidus conceptuels du livre) ───────────────
    unresolved = living_state.get("unresolved_tensions", [])
    if isinstance(unresolved, list) and unresolved:
        payload.setdefault("unresolved_tensions", unresolved)

    # ── 7. Tensions inter-livres ───────────────────────────────────────────────
    inter_tensions = living_state.get("inter_book_tensions_new") or \
                     living_state.get("inter_book_tension_signal")
    if isinstance(inter_tensions, Mapping) and inter_tensions:
        payload.setdefault("inter_book_tension_signal", inter_tensions)

    # ── 8. Stabilisateur de présence (concepts forcés à la surface) ───────────
    stabilizer = living_state.get("living_presence_stabilizer")
    if isinstance(stabilizer, Mapping) and stabilizer:
        payload.setdefault("living_presence_stabilizer", stabilizer)

    # ── 9. Opinion engine (positions sur les sujets du livre) ─────────────────
    opinion = living_state.get("opinion_engine") or living_state.get("opinion_signal")
    if isinstance(opinion, Mapping) and opinion:
        payload.setdefault("opinion_signal", opinion)

    # ── 10. Extraction de propositions (thèses du livre) ──────────────────────
    propositions = living_state.get("last_proposition_extraction")
    if isinstance(propositions, Mapping) and propositions:
        payload.setdefault("proposition_signal", propositions)

    # ── 11. Affect du livre (valence émotionnelle) ─────────────────────────────
    book_affect = living_state.get("last_book_affect")
    if isinstance(book_affect, Mapping) and book_affect:
        payload.setdefault("book_affect", book_affect)

    return payload


def extract_book_concepts(living_state: Mapping[str, Any]) -> list[str]:
    """
    Extrait une liste plate des concepts les plus importants des livres lus.
    Utile pour déboguer ou construire un contexte rapide.
    """
    concepts = []

    def add(x: Any) -> None:
        if isinstance(x, str) and len(x) > 3:
            concepts.append(x.lower().strip())
        elif isinstance(x, list):
            for item in x[:20]:
                add(item)
        elif isinstance(x, Mapping):
            for key in ("label", "concept", "name", "from", "to", "source", "target"):
                if key in x:
                    add(x[key])

    # Depuis last_book_synthesis
    synth = living_state.get("last_book_synthesis", {})
    if isinstance(synth, Mapping):
        add(synth.get("axes"))
        add(synth.get("top_keywords"))
        add(synth.get("main_concepts"))

    # Depuis book_understanding
    bu = living_state.get("book_understanding", {})
    if isinstance(bu, Mapping):
        add(bu.get("axes"))
        add(bu.get("keywords"))
        add(bu.get("question_axes"))

    # Depuis lexical_impregnation
    lex = living_state.get("lexical_impregnation", {})
    if isinstance(lex, Mapping):
        for w in (lex.get("top") or [])[:10]:
            if isinstance(w, Mapping):
                add(w.get("surface"))

    return list(dict.fromkeys(c for c in concepts if c))[:30]
