#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
leia_unified_connector.py — Hub central de connexion pour Leia V20+
═══════════════════════════════════════════════════════════════════════════════
Câble ensemble :
  • Les nouveaux modules (global_workspace, semantic_cortex, nlp_integration_pure,
    leia_comprehension_vivante, integration_cortex_workspace)
  • Les anciens modules vivants (affect_lexicon, living_language_generator,
    emergent_french_weaver, background_life_thread, spontaneous_impulse...)
  • Le lecteur PDF natif (leia_pure_pdf_reader → LeiaPDFV20Connector)

Expose LeiaLivingCore — drop-in compatible avec leia_complete_interface.py.

Différences V20+ vs stub original :
  1. SemanticCortex instancié → compréhension structurale profonde dans respond()
  2. load_pdf_book() connecté réellement via LeiaPDFV20Connector
  3. respond() passe les messages aussi par le cortex si workspace.ingest_structure() dispo
  4. snapshot() inclut les infos PDF et cortex
"""

from __future__ import annotations

import json
import math
import os
import random
import sys
import threading
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

# ═══════════════════════════════════════════════════════════════════════════════
# 0. CHEMINS
# ═══════════════════════════════════════════════════════════════════════════════

HERE = os.path.dirname(os.path.abspath(__file__))

if HERE not in sys.path:
    sys.path.insert(0, HERE)

# Anciens modules dans sous-dossiers organisés
for _subdir in ("Cerveau", "Coeur", "Conscience", "Cognition", "Initiative",
                "Memory", "Parler", "Soi_Leia", "Connaissance", "Interface"):
    _p = os.path.join(HERE, _subdir)
    if os.path.isdir(_p) and _p not in sys.path:
        sys.path.insert(0, _p)

# Dossier "A ajouté" (nouveaux modules)
for _candidate in ("A ajouté", "A ajout\u00e9", "A_ajoute", "nouveaux"):
    _p = os.path.join(HERE, _candidate)
    if os.path.isdir(_p) and _p not in sys.path:
        sys.path.insert(0, _p)
        break

# Fallback legacy flat
LEGACY = os.path.join(HERE, "leia_modules")
if os.path.isdir(LEGACY) and LEGACY not in sys.path:
    sys.path.insert(0, LEGACY)

# ═══════════════════════════════════════════════════════════════════════════════
# 1. IMPORTS NOUVEAUX (A ajouté)
# ═══════════════════════════════════════════════════════════════════════════════

from global_workspace import workspace, GlobalWorkspace
from nlp_integration_pure import LeiaNLPBridge, engine as nlp_engine
from leia_comprehension_vivante import comprendre

# SemanticCortex — compréhension structurale profonde (V20)
try:
    from semantic_cortex import SemanticCortex
    _CORTEX_OK = True
except Exception as _e_cortex:
    SemanticCortex = None  # type: ignore
    _CORTEX_OK = False

# CognitiveWorkspace — workspace enrichi qui comprend les CognitiveStructure
try:
    from integration_cortex_workspace import CognitiveWorkspace
    _COG_WS_OK = True
except Exception as _e_cog_ws:
    CognitiveWorkspace = None  # type: ignore
    _COG_WS_OK = False

# ═══════════════════════════════════════════════════════════════════════════════
# 2. IMPORT PDF V20 — zéro dépendance externe
# ═══════════════════════════════════════════════════════════════════════════════

try:
    from leia_pure_pdf_reader import LeiaPDFV20Connector, LeiaPurePDFReader
    _PDF_OK = True
except Exception as _e_pdf:
    LeiaPDFV20Connector = None  # type: ignore
    LeiaPurePDFReader = None    # type: ignore
    _PDF_OK = False

# ═══════════════════════════════════════════════════════════════════════════════
# 3. IMPORTS ANCIENS (modules vivants conservés)
# ═══════════════════════════════════════════════════════════════════════════════

try:
    from affect_lexicon import AffectLexicon
    _AFFECT_OK = True
except Exception:
    AffectLexicon = None  # type: ignore
    _AFFECT_OK = False

try:
    from living_language_generator import LivingLanguageGenerator, GenerationResult
    _GEN_OK = True
except Exception:
    LivingLanguageGenerator = None  # type: ignore
    GenerationResult = None  # type: ignore
    _GEN_OK = False

try:
    from background_life_thread import LeiaBackgroundLife
    _BG_OK = True
except Exception:
    LeiaBackgroundLife = None  # type: ignore
    _BG_OK = False

try:
    from emergent_french_weaver import EmergentFrenchWeaver
    _WEAVER_OK = True
except Exception:
    EmergentFrenchWeaver = None  # type: ignore
    _WEAVER_OK = False

try:
    from spontaneous_impulse import SpontaneousImpulse  # type: ignore
    _IMPULSE_OK = True
except Exception:
    SpontaneousImpulse = None  # type: ignore
    _IMPULSE_OK = False

# ═══════════════════════════════════════════════════════════════════════════════
# 4. HUB CENTRAL — LeiaLivingCore V20
# ═══════════════════════════════════════════════════════════════════════════════

class LeiaLivingCore:
    """
    Hub central V20. Drop-in replacement pour leia_living_core.py historique.

    Nouveau en V20 :
      - SemanticCortex → structures cognitives profondes dans respond() ET load_pdf_book()
      - LeiaPDFV20Connector → lecture PDF native, zéro lib externe
      - Si CognitiveWorkspace disponible : workspace.ingest_structure(cs) au lieu de inject_perception
    """

    def __init__(self, user_id: str = "default", auto_start_idle: bool = False):
        self.user_id = user_id
        self.started_at = time.time()
        self.messages_exchanged = 0
        self.last_user_message = ""
        self.last_leia_response = ""
        self._idle_running = False
        self._idle_thread: Optional[threading.Thread] = None
        self._idle_stop = threading.Event()

        # ── NLP + Workspace (nouveaux) ─────────────────────────────────────
        self.nlp = LeiaNLPBridge()
        self.workspace = workspace  # singleton global

        # ── Cortex sémantique (V20) ────────────────────────────────────────
        self.cortex = SemanticCortex() if _CORTEX_OK else None

        # Détermine si le workspace supporte ingest_structure()
        self._ws_has_ingest = callable(getattr(self.workspace, "ingest_structure", None))

        # ── Affect Lexicon ─────────────────────────────────────────────────
        self.affect = AffectLexicon() if _AFFECT_OK else None

        # ── Générateur de langage ──────────────────────────────────────────
        if _GEN_OK:
            self.generator = LivingLanguageGenerator()
            try:
                self.generator._verbose = False  # type: ignore
            except Exception:
                pass
        else:
            self.generator = None

        # ── Weaver ────────────────────────────────────────────────────────
        self.weaver = EmergentFrenchWeaver() if _WEAVER_OK else None

        # ── Background life ────────────────────────────────────────────────
        self._bg_life: Optional[Any] = None
        if _BG_OK:
            try:
                self._bg_life = LeiaBackgroundLife(self, interval_seconds=20.0)
            except Exception:
                pass

        # ── Spontaneous impulse ────────────────────────────────────────────
        self._impulse = SpontaneousImpulse() if _IMPULSE_OK else None

        # ── PDF V20 ────────────────────────────────────────────────────────
        if _PDF_OK:
            self._pdf = LeiaPDFV20Connector(
                cortex=self.cortex,
                workspace=self.workspace,
            )
        else:
            self._pdf = None

        # Statistiques PDF de session
        self._pdf_sessions: List[Dict[str, Any]] = []

        # ── Persistance ────────────────────────────────────────────────────
        self._persist_dir = os.path.join(HERE, "leia_data")
        os.makedirs(self._persist_dir, exist_ok=True)
        self._state_path = os.path.join(self._persist_dir, f"state_{user_id}.json")

        if auto_start_idle:
            self.start_idle_cycle(20.0)

    # ── API INTERFACE ──────────────────────────────────────────────────────

    def respond(self, user_message: str) -> str:
        """
        Pipeline complet V20 :
        1. NLP pur Python    → signal rapide
        2. SemanticCortex    → structure cognitive profonde  [NOUVEAU V20]
        3. Workspace         → ingest_structure() ou inject_perception()
        4. Affect lexicon    → enrichissement émotionnel
        5. Génération        → living_language_generator
        6. Libération        → après_expression()
        """
        if not user_message or not user_message.strip():
            return "…"

        self.last_user_message = user_message.strip()
        self.messages_exchanged += 1

        # ── 1. NLP rapide ──────────────────────────────────────────────────
        sig = self.nlp.signal(user_message)

        # ── 2. Cortex sémantique (V20) ─────────────────────────────────────
        if self.cortex is not None:
            try:
                cs = self.cortex.process(user_message, source="dialogue")
                # Workspace V20 : ingest_structure si disponible
                if self._ws_has_ingest:
                    self.workspace.ingest_structure(cs, source="dialogue")
                else:
                    # Fallback : inject_perception avec le signal NLP
                    self.workspace.inject_perception(sig)
            except Exception:
                # Dégradation gracieuse vers V19
                try:
                    self.workspace.inject_perception(sig)
                except Exception:
                    pass
        else:
            # Pas de cortex → V19 pur
            try:
                self.workspace.inject_perception(sig)
            except Exception:
                pass

        # ── 3. Affect lexicon ──────────────────────────────────────────────
        if self.affect:
            try:
                aff = self.affect.analyze(user_message)  # type: ignore
                valence = float(aff.get("valence", 0.0))
                if abs(valence) > 0.3:
                    self.workspace.inject_emotion(valence, source="affect_lexicon")
            except Exception:
                pass

        # ── 4. Payload + living_state ──────────────────────────────────────
        payload = self.workspace.payload_pour_expression()
        gcf = self.workspace.vers_global_conscious_field_state()
        living_state = self._build_living_state(payload, gcf)

        # ── 5. Génération ──────────────────────────────────────────────────
        if self.generator:
            try:
                result = self.generator.generate(
                    user_message=user_message,
                    living_state=living_state,
                    self_memory=[],
                    active_impulses=payload.get("themes_obsedants", []),
                    emotional_pressure=payload.get("pression_totale", 0.3),
                    causal_memory=[],
                    max_attempts=5,
                    temperature=0.55,
                    response_constraint=None,
                )
                text = str(result.text or "").strip()
            except Exception:
                text = self._fallback_generate(payload)
        else:
            text = self._fallback_generate(payload)

        if not text:
            text = "…"
        self.last_leia_response = text

        # ── 6. Post-expression ─────────────────────────────────────────────
        try:
            self.workspace.après_expression(fraction_liberation=0.5)
        except Exception:
            pass
        try:
            self.workspace.tick(elapsed=2.0)
        except Exception:
            pass

        return text

    def autonomous_speak_if_ready(self, force: bool = False) -> Optional[str]:
        """Si la pression expressive est forte, Leia parle d'elle-même."""
        pression = self.workspace.pression_expressive()
        if not force and pression < 0.45:
            return None

        payload = self.workspace.payload_pour_expression()
        gcf = self.workspace.vers_global_conscious_field_state()
        living_state = self._build_living_state(payload, gcf)

        if self.generator:
            try:
                result = self.generator.generate(
                    user_message=" ",
                    living_state=living_state,
                    self_memory=[],
                    active_impulses=payload.get("themes_obsedants", []),
                    emotional_pressure=pression,
                    causal_memory=[],
                    max_attempts=4,
                    temperature=0.6,
                )
                text = str(result.text or "").strip()
                if text:
                    self.workspace.après_expression(fraction_liberation=0.3)
                    return text
            except Exception:
                pass
        return None

    # ── PDF V20 ────────────────────────────────────────────────────────────

    def load_pdf_book(
        self,
        path: str,
        progress_callback=None,
        max_pages: Optional[int] = None,
        start_page: int = 1,
    ) -> Dict[str, Any]:
        """
        Charge et digère un PDF dans le système V20.

        Pipeline :
            Bytes PDF → parseur natif (zéro dépendance)
                ↓ page par page
            SemanticCortex.process(fragment) → CognitiveStructure
                ↓
            workspace.ingest_structure(cs)
                ↓
            Graphe causal + tensions + scènes actives dans le workspace

        Retourne un rapport complet compatible avec leia_complete_interface.py.
        """
        if self._pdf is None:
            return {
                "ok": False,
                "error": "leia_pure_pdf_reader.py non trouvé — placez-le dans Connaissance/",
                "path": path,
            }

        result = self._pdf.load_pdf_book(
            path,
            progress_callback=progress_callback,
            max_pages=max_pages,
            start_page=start_page,
        )

        # Enregistre la session pour snapshot()
        self._pdf_sessions.append({
            "path": path,
            "ok": result.get("ok", False),
            "pages_read": result.get("pages_read", 0),
            "chunks": result.get("chunks_count", 0),
            "cognitive_structures": result.get("cognitive_structures", 0),
            "workspace_integrations": result.get("workspace_integrations", 0),
            "ts": time.time(),
        })

        # Tick après lecture pour déclencher émergences
        try:
            self.workspace.tick(elapsed=10.0)
        except Exception:
            pass

        return result

    def get_pdf_info(self, path: str) -> Dict[str, Any]:
        """Infos rapides sur un PDF sans l'ingérer."""
        if LeiaPurePDFReader is None:
            return {"ok": False, "error": "leia_pure_pdf_reader non disponible"}
        result = LeiaPurePDFReader.get_info(path)
        result["ok"] = result.get("success", False)
        return result

    # ── ÉTAT / SNAPSHOT ────────────────────────────────────────────────────

    def snapshot(self) -> Dict[str, Any]:
        """État global pour l'interface graphique."""
        ws = self.workspace.snapshot()
        return {
            "ok": True,
            "user_id": self.user_id,
            "messages_exchanged": self.messages_exchanged,
            "workspace": ws,
            "emotional_tone": ws.get("emotion", {}).get("tonalite", "neutre"),
            "dominant_thought": ws.get("pensee_dominante", {}),
            "concepts_actifs": ws.get("concepts_actifs", []),
            "pression": ws.get("pression", {}),
            "pdf_sessions": len(self._pdf_sessions),
            "last_pdf": self._pdf_sessions[-1] if self._pdf_sessions else None,
            "modules": {
                "semantic_cortex": _CORTEX_OK,
                "cognitive_workspace": _COG_WS_OK,
                "pdf_v20": _PDF_OK,
                "affect_lexicon": _AFFECT_OK,
                "living_language_generator": _GEN_OK,
                "emergent_weaver": _WEAVER_OK,
                "background_life": _BG_OK,
                "spontaneous_impulse": _IMPULSE_OK,
            },
        }

    def get_state_snapshot(self) -> Dict[str, Any]:
        return self.snapshot()

    def self_test(self) -> Dict[str, Any]:
        errors: List[str] = []
        warnings: List[str] = []
        if not _GEN_OK:
            errors.append("living_language_generator non chargé")
        if not _AFFECT_OK:
            errors.append("affect_lexicon non chargé")
        if not _CORTEX_OK:
            warnings.append("semantic_cortex absent — compréhension structurale désactivée")
        if not _PDF_OK:
            warnings.append("leia_pure_pdf_reader absent — lecture PDF désactivée")
        if not _COG_WS_OK:
            warnings.append("integration_cortex_workspace absent — ingest_structure() désactivé")
        return {
            "ok": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
        }

    # ── IDLE / BACKGROUND LIFE ─────────────────────────────────────────────

    def start_idle_cycle(self, interval_seconds: float = 20.0) -> None:
        if self._idle_running:
            return
        self._idle_running = True
        self._idle_stop.clear()
        self._idle_thread = threading.Thread(
            target=self._idle_loop,
            args=(interval_seconds,),
            daemon=True,
            name="LeiaIdle",
        )
        self._idle_thread.start()

    def stop_idle_cycle(self) -> None:
        self._idle_running = False
        self._idle_stop.set()

    def _idle_loop(self, interval: float) -> None:
        while self._idle_running and not self._idle_stop.is_set():
            try:
                self.workspace.tick(elapsed=interval)
            except Exception:
                pass
            if random.random() < 0.05:
                self._save_state()
            self._idle_stop.wait(timeout=interval)

    # ── COMPATIBILITÉ background_life_thread.py ────────────────────────────

    def tick_inner_life(self) -> Dict[str, Any]:
        try:
            self.workspace.tick(elapsed=20.0)
        except Exception:
            pass
        p = None
        try:
            p = self.workspace.pensee_dominante()
        except Exception:
            pass
        return {
            "tick_ok": True,
            "dominant_thought": (p.contenu[:60] if p else None),
            "emotion": self.workspace.champ_emotionnel.tonalite(),
        }

    def consolidate_memories(self) -> Dict[str, Any]:
        try:
            self.workspace.sauvegarder(self._state_path)
        except Exception:
            pass
        return {"consolidated": True, "path": self._state_path}

    def dream_fragments(self) -> List[str]:
        th = self.workspace.monologue.themes_dominants(5)
        q = self.workspace.monologue.questions_flottantes[:3]
        return [f"thème: {t}" for t in th] + [f"question: {q_}" for q_ in q]

    # ── UTILITAIRES INTERNES ───────────────────────────────────────────────

    def _build_living_state(self, payload: Dict[str, Any], gcf: Dict[str, Any]) -> Dict[str, Any]:
        """Convertit le payload workspace en living_state pour living_language_generator."""
        tone = payload.get("emotional_tone", "neutre")
        tension = float(payload.get("tension", 0.0))
        energy = float(payload.get("energy", 0.8))
        fatigue = float(payload.get("fatigue", 0.0))
        resonance = float(payload.get("resonance", 0.0))
        pression = float(payload.get("pression_totale", 0.3))

        register = "neutre"
        if tone in ("vive", "ouverte"):
            register = "vif"
        elif tone in ("sombre", "mélancolique"):
            register = "grave"
        elif tone == "épuisée":
            register = "doux"
        elif tone == "tendue":
            register = "incertain"

        return {
            "tonalite": tone,
            "register": register,
            "valence": tension,
            "tension": tension,
            "energy": energy,
            "fatigue": fatigue,
            "resonance": resonance,
            "pression": pression,
            "rhythm_shortness": 0.3 + fatigue * 0.4,
            "rhythm_ellipsis": 0.2 + resonance * 0.3,
            "rhythm_rupture": tension * 0.6,
            "dominant_concepts": payload.get("focus_concepts", []),
            "active_tensions": payload.get("active_tensions", []),
        }

    def _fallback_generate(self, payload: Dict[str, Any]) -> str:
        """Génération symbolique directe si living_language_generator absent."""
        tone = payload.get("emotional_tone", "neutre")
        concepts = payload.get("focus_concepts", [])
        tensions = payload.get("active_tensions", [])
        questions = payload.get("questions_flottantes", [])
        parts: List[str] = []
        if concepts:
            parts.append(f"Je réfléchis à {' '.join(concepts[:3])}.")
        if tensions:
            a, b = tensions[0]
            parts.append(f"Il y a quelque chose entre {a} et {b}.")
        if questions:
            parts.append(f"Une question me hante : {questions[0]} ?")
        if not parts:
            parts.append("Je suis là, en silence.")
        text = " ".join(parts)
        if tone == "sombre":
            text = text.rstrip(".") + "…"
        elif tone == "vive":
            text = text.rstrip(".") + " !"
        return text

    def _save_state(self) -> None:
        try:
            self.workspace.sauvegarder(self._state_path)
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════════════════════════
# POINT D'ENTRÉE CONSOLE
# ═══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    print("═" * 70)
    print("  LEIA — Hub unifié V20")
    print("  Pure Python · SemanticCortex · PDF natif · Zéro LLM")
    print("═" * 70)

    core = LeiaLivingCore(user_id="console", auto_start_idle=True)
    st = core.self_test()

    print(f"\n  Statut modules :")
    for k, v in core.snapshot()["modules"].items():
        icon = "✓" if v else "✗"
        print(f"    {icon} {k}")
    if st.get("errors"):
        print(f"\n  Erreurs : {st['errors']}")
    if st.get("warnings"):
        print(f"  Avertissements : {st['warnings']}")

    print(f"\n  Commandes : 'quit', 'état', 'pdf <chemin>', 'info <chemin>'")
    print("─" * 70)

    while True:
        try:
            user_text = input("\nToi > ").strip()
        except (EOFError, KeyboardInterrupt):
            break

        if not user_text:
            continue
        if user_text.lower() in ("quit", "exit", "q"):
            break
        if user_text.lower() in ("état", "etat", "state", "snapshot"):
            snap = core.snapshot()
            print(json.dumps(snap, ensure_ascii=False, indent=2)[:2000])
            continue
        if user_text.lower().startswith("pdf "):
            pdf_path = user_text[4:].strip()
            print(f"  Lecture de {pdf_path}…")
            res = core.load_pdf_book(pdf_path, progress_callback=lambda m: print(f"  {m}"))
            print(f"  Résultat : ok={res.get('ok')} | pages={res.get('pages_read')} | "
                  f"structures={res.get('cognitive_structures')} | ws={res.get('workspace_integrations')}")
            continue
        if user_text.lower().startswith("info "):
            pdf_path = user_text[5:].strip()
            print(json.dumps(core.get_pdf_info(pdf_path), ensure_ascii=False, indent=2))
            continue

        response = core.respond(user_text)
        print(f"Leia > {response}")

    core.stop_idle_cycle()
    core.consolidate_memories()
    print("\n  Session terminée. État sauvegardé.")
    print("═" * 70)


if __name__ == "__main__":
    main()
