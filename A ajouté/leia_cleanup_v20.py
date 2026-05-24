#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
leia_cleanup_v20.py — Script de nettoyage / migration vers V20

Ce script :
  1. Crée un dossier _legacy/ et y déplace les fichiers obsolètes
  2. Vérifie la présence des fichiers V20 essentiels
  3. Génère un rapport de migration
  4. NE SUPPRIME RIEN — tout est dans _legacy/, récupérable

Usage :
    python leia_cleanup_v20.py              # simulation (dry-run)
    python leia_cleanup_v20.py --apply      # applique vraiment
    python leia_cleanup_v20.py --report     # rapport seulement
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, List, Tuple

# ─── Table des fichiers obsolètes ─────────────────────────────────────────────
# Chaque entrée : (dossier_source, nom_fichier, raison)

OBSOLETE: List[Tuple[str, str, str]] = [
    # Cerveau — remplacés par leia_unified_connector + global_workspace_v2
    ("Cerveau", "leia_living_core.py",       "Remplacé par leia_unified_connector.py"),
    ("Cerveau", "living_attention.py",        "Intégré dans global_workspace_v2"),
    ("Cerveau", "unified_lived_experience.py","Remplacé par global_workspace_v2"),
    ("Cerveau", "nlp_integration.py",         "Remplacé par nlp_integration_pure.py (zéro spaCy)"),
    # Cognition — remplacés par semantic_cortex
    ("Cognition", "user_utterance_parser.py", "Remplacé par semantic_cortex.process()"),
    ("Cognition", "proposition_extractor.py", "Remplacé par semantic_cortex.process()"),
    ("Cognition", "book_understanding_engine.py", "Remplacé par semantic_cortex + workspace"),
    ("Cognition", "concept_relation_engine.py",   "Remplacé par leia_comprehension_vivante"),
    # Conscience — remplacés par global_workspace_v2
    ("Conscience", "persistent_subjective_life_engine.py", "Remplacé par global_workspace_v2 (monologue + profondeurs)"),
    ("Conscience", "subjective_response_integrator.py",    "Remplacé par connector._build_living_state()"),
    # Memory — mémoires plates remplacées par workspace interne
    ("Memory", "associative_memory.py", "Propagation intégrée dans global_workspace_v2"),
    ("Memory", "causal_memory_engine.py","Liens causaux intégrés dans CognitiveWorkspace"),
    ("Memory", "vector_memory.py",       "Inutile sans LLM/embedding externe"),
    # Parler — redondants avec le connector
    ("Parler", "living_expression_engine.py",   "Fusionné dans connector._build_living_state()"),
    ("Parler", "state_language_bridge_patch.py", "Remplacé par connector"),
    ("Parler", "conversation_window.py",         "Géré par Interface/leia_complete_interface.py"),
    # Connaissance — remplacés par leia_pure_pdf_reader
    ("Connaissance", "deep_book_digestion.py",  "Remplacé par LeiaPDFV20Connector"),
    # Racine — anciens ponts
    (".",  "leia_spacy_engine.py", "Remplacé par nlp_integration_pure.py"),
    (".",  "leia_book_patch.py",   "Remplacé par connector + PDF V20"),
]

# ─── Fichiers V20 essentiels à vérifier ───────────────────────────────────────

REQUIRED_V20: List[Tuple[str, str, str]] = [
    # (dossier, fichier, description)
    ("A ajouté", "semantic_cortex.py",            "Cortex sémantique profond"),
    ("A ajouté", "global_workspace_v2.py",         "Conscience active V2"),
    ("A ajouté", "integration_cortex_workspace.py","CognitiveWorkspace (ingest_structure)"),
    ("A ajouté", "nlp_integration_pure.py",        "Pont NLP zéro dépendance"),
    ("A ajouté", "leia_comprehension_vivante.py",  "Mémoire sémantique persistante"),
    ("A ajouté", "leia_unified_connector.py",      "Hub central V20"),
    ("Connaissance", "leia_pure_pdf_reader.py",    "Lecteur PDF natif zéro dépendance"),
    (".", "run_leia_ui.py",                         "Point d'entrée UI"),
    ("Interface", "leia_complete_interface.py",    "Interface Tkinter"),
]

# ─── Fichiers à conserver impérativement (ne pas toucher) ─────────────────────

KEEP: List[Tuple[str, str]] = [
    ("Cerveau",     "conflict_capacity.py"),
    ("Coeur",       "affect_lexicon.py"),
    ("Coeur",       "value_conflict_engine.py"),
    ("Coeur",       "relational_stakes_engine.py"),
    ("Coeur",       "user_model.py"),
    ("Conscience",  "internal_imagination_engine.py"),
    ("Conscience",  "situated_presence.py"),
    ("Conscience",  "long_living_dynamics_engine.py"),
    ("Cognition",   "reasoning_trace.py"),
    ("Cognition",   "opinion_engine.py"),
    ("Cognition",   "semantic_coherence.py"),
    ("Initiative",  "natural_initiative.py"),
    ("Initiative",  "strong_initiative_engine.py"),
    ("Initiative",  "rhythmic_impregnation.py"),
    ("Memory",      "memory_hierarchy.py"),
    ("Memory",      "reading_living_consolidation_engine.py"),
    ("Memory",      "semantic_plasticity.py"),
    ("Memory",      "autobiographical_continuity_engine.py"),
    ("Memory",      "affective_memory.py"),
    ("Parler",      "living_language_generator.py"),
    ("Parler",      "emergent_french_weaver.py"),
    ("Parler",      "lexical_impregnation.py"),
    ("Soi_Leia",    "self_model.py"),
    ("Soi_Leia",    "self_evaluation_loop.py"),
    ("Soi_Leia",    "self_monitoring_filter.py"),
    ("Connaissance","inter_book_tension_engine.py"),
    ("Connaissance","pdf_knowledge_engine.py"),   # garde — wrapper compat
    ("Connaissance","leia_pure_pdf_reader.py"),   # le nouveau lecteur
]


def _find_root() -> Path:
    """Trouve la racine du projet Leia (dossier contenant Interface/)."""
    candidates = [
        Path(__file__).parent,
        Path("."),
        Path(os.environ.get("LEIA_ROOT", ".")),
    ]
    for c in candidates:
        if (c / "Interface").is_dir() or (c / "Cerveau").is_dir():
            return c.resolve()
    return Path(".").resolve()


def _color(text: str, code: str) -> str:
    """ANSI colors si terminal le supporte."""
    if sys.stdout.isatty():
        return f"\033[{code}m{text}\033[0m"
    return text


def ok(s: str) -> str:  return _color(s, "32")
def warn(s: str) -> str: return _color(s, "33")
def err(s: str) -> str:  return _color(s, "31")
def bold(s: str) -> str: return _color(s, "1")
def dim(s: str) -> str:  return _color(s, "2")


def run(root: Path, apply: bool, report_only: bool) -> Dict:
    """Exécute l'analyse et (si apply=True) la migration."""

    print(bold(f"\n{'═' * 64}"))
    print(bold("  LEIA V20 — Script de migration / nettoyage"))
    print(bold(f"  Racine : {root}"))
    print(bold(f"  Mode   : {'APPLICATION RÉELLE' if apply else 'SIMULATION (dry-run)'}"))
    print(bold(f"{'═' * 64}\n"))

    legacy_dir = root / "_legacy"
    results = {
        "root": str(root),
        "apply": apply,
        "moved": [],
        "missing_obsolete": [],
        "v20_present": [],
        "v20_missing": [],
        "kept": [],
    }

    # ── 1. Vérification des fichiers V20 essentiels ─────────────────────────
    print(bold("1. FICHIERS V20 ESSENTIELS"))
    print("─" * 64)

    all_v20_present = True
    for folder, fname, desc in REQUIRED_V20:
        candidates = [
            root / folder / fname,
            root / f"A ajout\u00e9" / fname,  # unicode fallback
            root / fname,                       # racine directe
        ]
        found = next((p for p in candidates if p.exists()), None)
        if found:
            print(f"  {ok('✓')} {folder}/{fname:<40} {dim(desc)}")
            results["v20_present"].append(f"{folder}/{fname}")
        else:
            print(f"  {err('✗')} {folder}/{fname:<40} {warn('MANQUANT')} — {desc}")
            results["v20_missing"].append(f"{folder}/{fname}")
            all_v20_present = False

    if not all_v20_present:
        print(f"\n  {warn('⚠ Certains fichiers V20 sont absents.')} "
              "Copiez-les avant de lancer --apply.\n")

    # ── 2. Fichiers à conserver (sanity check) ──────────────────────────────
    print(f"\n{bold('2. FICHIERS CONSERVÉS (non touchés)')}")
    print("─" * 64)

    for folder, fname in KEEP:
        p = root / folder / fname
        if p.exists():
            print(f"  {ok('✓')} {folder}/{fname}")
            results["kept"].append(f"{folder}/{fname}")
        else:
            print(f"  {dim('·')} {folder}/{fname:<45} {dim('(absent, non critique)')}")

    # ── 3. Fichiers obsolètes ───────────────────────────────────────────────
    print(f"\n{bold('3. FICHIERS OBSOLÈTES → _legacy/')}")
    print("─" * 64)

    for folder, fname, reason in OBSOLETE:
        src = root / folder / fname
        if not src.exists():
            print(f"  {dim('·')} {folder}/{fname:<42} {dim('(déjà absent)')}")
            results["missing_obsolete"].append(f"{folder}/{fname}")
            continue

        dst_dir = legacy_dir / folder
        dst = dst_dir / fname

        if not report_only:
            if apply:
                dst_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(src), str(dst))
                print(f"  {ok('→')} {folder}/{fname:<42} {dim(reason[:50])}")
            else:
                print(f"  {warn('~')} {folder}/{fname:<42} {dim('[serait déplacé]')} {dim(reason[:45])}")
        else:
            print(f"  {warn('·')} {folder}/{fname:<42} {dim(reason[:50])}")

        results["moved"].append({
            "src": str(src.relative_to(root)),
            "dst": str(dst.relative_to(root)) if apply else f"_legacy/{folder}/{fname}",
            "reason": reason,
        })

    # ── 4. Nettoyage __pycache__ ─────────────────────────────────────────────
    print(f"\n{bold('4. NETTOYAGE __pycache__')}")
    print("─" * 64)

    pycaches = list(root.rglob("__pycache__"))
    pycs = list(root.rglob("*.pyc"))

    print(f"  Dossiers __pycache__ : {len(pycaches)}")
    print(f"  Fichiers .pyc        : {len(pycs)}")

    if apply:
        cleaned = 0
        for pc in pycaches:
            try:
                shutil.rmtree(pc)
                cleaned += 1
            except Exception:
                pass
        print(f"  {ok(f'✓ {cleaned} dossiers __pycache__ supprimés')}")
    else:
        print(f"  {dim('[simulation] seraient supprimés si --apply')}")

    # ── 5. Rapport final ──────────────────────────────────────────────────────
    print(f"\n{bold('═' * 64)}")
    print(bold("  RÉSUMÉ"))
    print(bold(f"{'═' * 64}"))
    print(f"  V20 présents     : {len(results['v20_present'])} / {len(REQUIRED_V20)}")
    print(f"  V20 manquants    : {len(results['v20_missing'])}")
    print(f"  Fichiers archivés: {len(results['moved'])} {'(réels)' if apply else '(simulation)'}")
    print(f"  Fichiers conservés: {len(results['kept'])}")

    if results["v20_missing"]:
        print(f"\n  {err('Fichiers V20 à fournir :')}")
        for f in results["v20_missing"]:
            print(f"    • {f}")

    report_path = root / "migration_v20_report.json"
    if apply or not report_only:
        try:
            report_path.write_text(
                json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            print(f"\n  {ok(f'✓ Rapport sauvegardé : {report_path}')}")
        except Exception as exc:
            print(f"\n  {warn(f'⚠ Rapport non sauvegardé : {exc}')}")

    if not apply and not report_only:
        print(f"\n  {warn('→ Lancez avec --apply pour appliquer les changements.')}")

    print()
    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Migration Leia V19 → V20 — archive les fichiers obsolètes"
    )
    parser.add_argument("--apply",   action="store_true", help="Applique les déplacements (sinon dry-run)")
    parser.add_argument("--report",  action="store_true", help="Rapport seulement, ne propose rien")
    parser.add_argument("--root",    type=str, default=None, help="Racine du projet (auto-détectée si absent)")
    args = parser.parse_args()

    root = Path(args.root).resolve() if args.root else _find_root()
    run(root, apply=args.apply, report_only=args.report)


if __name__ == "__main__":
    main()
