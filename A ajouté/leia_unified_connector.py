#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
leia_unified_connector.py — Hub central de connexion pour Leia V20+
═══════════════════════════════════════════════════════════════════════════════
Câble ensemble :
  • Les 3 nouveaux modules (global_workspace, nlp_integration_pure, leia_comprehension_vivante)
  • Les anciens modules vivants (affect_lexicon, living_language_generator, emergent_french_weaver,
    background_life_thread, spontaneous_impulse...)

Expose LeiaLivingCore — drop-in compatible avec leia_complete_interface.py.
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
# 0. CHEMINS — tout mettre dans sys.path
# ═══════════════════════════════════════════════════════════════════════════════

HERE = os.path.dirname(os.path.abspath(__file__))

# Les 3 nouveaux fichiers sont à la racine du workspace
if HERE not in sys.path:
    sys.path.insert(0, HERE)

# Les anciens modules téléchargés localement
LEGACY = os.path.join(HERE, "leia_modules")
if os.path.isdir(LEGACY) and LEGACY not in sys.path:
    sys.path.insert(0, LEGACY)

# ═══════════════════════════════════════════════════════════════════════════════
# 1. IMPORTS NOUVEAUX (A ajouté)
# ═══════════════════════════════════════════════════════════════════════════════

from global_workspace import workspace, GlobalWorkspace
from nlp_integration_pure import LeiaNLPBridge, engine as nlp_engine
from leia_comprehension_vivante import comprendre

# ═══════════════════════════════════════════════════════════════════════════════
# 2. IMPORTS ANCIENS (modules vivants déjà existants)
# ═══════════════════════════════════════════════════════════════════════════════

try:
    from affect_lexicon import AffectLexicon
    _AFFECT_OK = True
except Exception as e:
    AffectLexicon = None  # type: ignore
    _AFFECT_OK = False

try:
    from living_language_generator import LivingLanguageGenerator, GenerationResult
    _GEN_OK = True
except Exception as e:
    LivingLanguageGenerator = None  # type: ignore
    GenerationResult = None  # type: ignore
    _GEN_OK = False

try:
    from background_life_thread import LeiaBackgroundLife
    _BG_OK = True
except Exception as e:
    LeiaBackgroundLife = None  # type: ignore
    _BG_OK = False

try:
    from emergent_french_weaver import EmergentFrenchWeaver
    _WEAVER_OK = True
except Exception as e:
    EmergentFrenchWeaver = None  # type: ignore
    _WEAVER_OK = False

try:
    from spontaneous_impulse import SpontaneousImpulse  # type: ignore
    _IMPULSE_OK = True
except Exception:
    SpontaneousImpulse = None  # type: ignore
    _IMPULSE_OK = False

# ═══════════════════════════════════════════════════════════════════════════════
# 3. HUB CENTRAL — LeiaLivingCore reconnecté
# ═══════════════════════════════════════════════════════════════════════════════

class LeiaLivingCore:
    """
    Drop-in replacement pour le leia_living_core.py historique.
    Tout passe par le global_workspace comme mémoire de travail vivante.
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

        # ── Composants NLP / Workspace (nouveaux) ──────────────────────────
        self.nlp = LeiaNLPBridge()
        self.workspace = workspace  # singleton global

        # ── Affect Lexicon (ancien) ────────────────────────────────────────
        self.affect = AffectLexicon() if _AFFECT_OK else None

        # ── Générateur de langage (ancien) ───────────────────────────────────
        if _GEN_OK:
            self.generator = LivingLanguageGenerator()
            # On désactive la log de debug interne bruyante si possible
            try:
                self.generator._verbose = False  # type: ignore
            except Exception:
                pass
        else:
            self.generator = None

        # ── Weaver (ancien) ────────────────────────────────────────────────
        self.weaver = EmergentFrenchWeaver() if _WEAVER_OK else None

        # ── Background life (ancien wrapper → nouveau tick) ────────────────
        self._bg_life: Optional[Any] = None
        if _BG_OK:
            try:
                self._bg_life = LeiaBackgroundLife(self, interval_seconds=20.0)
            except Exception:
                pass

        # ── Spontaneous impulse ────────────────────────────────────────────
        self._impulse = SpontaneousImpulse() if _IMPULSE_OK else None

        # ── Persistance légère ─────────────────────────────────────────────
        self._persist_dir = os.path.join(HERE, "leia_data")
        os.makedirs(self._persist_dir, exist_ok=True)
        self._state_path = os.path.join(self._persist_dir, f"state_{user_id}.json")

        if auto_start_idle:
            self.start_idle_cycle(20.0)

    # ── API INTERFACE (attendues par leia_complete_interface.py) ───────────

    def respond(self, user_message: str) -> str:
        """
        Pipeline complet :
        1. NLP pur Python (comprendre le message)
        2. Injection dans le workspace (mémoire vivante)
        3. Analyse affective (ancien affect_lexicon)
        4. Génération symbolique (living_language_generator)
        5. Libération de la pression expressive
        """
        if not user_message or not user_message.strip():
            return "…"

        self.last_user_message = user_message.strip()
        self.messages_exchanged += 1

        # ── 1. NLP ─────────────────────────────────────────────────────────
        sig = self.nlp.signal(user_message)

        # ── 2. Workspace ─────────────────────────────────────────────────────
        self.workspace.inject_perception(sig)

        # ── 3. Affect lexicon (enrichissement émotionnel) ──────────────────────
        extra_emotion = 0.0
        if self.affect:
            try:
                aff = self.affect.analyze(user_message)  # type: ignore
                valence = float(aff.get("valence", 0.0))
                if abs(valence) > 0.3:
                    extra_emotion = valence
                    self.workspace.inject_emotion(valence, source="affect_lexicon")
            except Exception:
                pass

        # ── 4. Construire le living_state pour le générateur ─────────────────
        payload = self.workspace.payload_pour_expression()
        gcf = self.workspace.vers_global_conscious_field_state()

        living_state = self._build_living_state(payload, gcf)

        # ── 5. Génération ────────────────────────────────────────────────────
        if self.generator:
            try:
                result = self.generator.generate(
                    user_message=user_message,
                    living_state=living_state,
                    self_memory=[],  # TODO: pont depuis workspace.monologue
                    active_impulses=payload.get("themes_obsedants", []),
                    emotional_pressure=payload.get("pression_totale", 0.3),
                    causal_memory=[],
                    max_attempts=5,
                    temperature=0.55,
                    response_constraint=None,
                )
                text = str(result.text or "").strip()
            except Exception as exc:
                text = self._fallback_generate(payload)
        else:
            text = self._fallback_generate(payload)

        # Nettoyage basique
        if not text:
            text = "…"
        self.last_leia_response = text

        # ── 6. Après expression ────────────────────────────────────────────────
        self.workspace.après_expression(fraction_liberation=0.5)

        # ── 7. Tick de fond ──────────────────────────────────────────────────
        self.workspace.tick(elapsed=2.0)

        return text

    def autonomous_speak_if_ready(self, force: bool = False) -> Optional[str]:
        """
        Si la pression expressive est forte, Leia parle d'elle-même.
        """
        pression = self.workspace.pression_expressive()
        if not force and pression < 0.45:
            return None

        payload = self.workspace.payload_pour_expression()
        gcf = self.workspace.vers_global_conscious_field_state()
        living_state = self._build_living_state(payload, gcf)

        # Message "vide" car c'est une parole autonome
        trigger = " "
        if self.generator:
            try:
                result = self.generator.generate(
                    user_message=trigger,
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
            "modules": {
                "affect_lexicon": _AFFECT_OK,
                "living_language_generator": _GEN_OK,
                "emergent_weaver": _WEAVER_OK,
                "background_life": _BG_OK,
                "spontaneous_impulse": _IMPULSE_OK,
            }
        }

    def get_state_snapshot(self) -> Dict[str, Any]:
        return self.snapshot()

    def self_test(self) -> Dict[str, Any]:
        errors: List[str] = []
        if not _GEN_OK:
            errors.append("living_language_generator non chargé")
        if not _AFFECT_OK:
            errors.append("affect_lexicon non chargé")
        return {"ok": len(errors) == 0, "errors": errors}

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
            name="LeiaIdle"
        )
        self._idle_thread.start()

    def stop_idle_cycle(self) -> None:
        self._idle_running = False
        self._idle_stop.set()

    def _idle_loop(self, interval: float) -> None:
        while self._idle_running and not self._idle_stop.is_set():
            self.workspace.tick(elapsed=interval)
            # Sauvegarde légère périodique
            if random.random() < 0.05:
                self._save_state()
            self._idle_stop.wait(timeout=interval)

    # ── API BACKGROUND LIFE (pour background_life_thread.py) ───────────────

    def tick_inner_life(self) -> Dict[str, Any]:
        self.workspace.tick(elapsed=20.0)
        p = self.workspace.pensee_dominante()
        return {
            "tick_ok": True,
            "dominant_thought": p.contenu[:60] if p else None,
            "emotion": self.workspace.champ_emotionnel.tonalite(),
        }

    def consolidate_memories(self) -> Dict[str, Any]:
        self.workspace.sauvegarder(self._state_path)
        return {"consolidated": True, "path": self._state_path}

    def dream_fragments(self) -> List[str]:
        th = self.workspace.monologue.themes_dominants(5)
        q = self.workspace.monologue.questions_flottantes[:3]
        return [f"thème: {t}" for t in th] + [f"question: {q_}" for q_ in q]

    # ── PDF / LECTURE (stub pour compatibilité) ────────────────────────────

    def load_pdf_book(self, path: str, progress_callback=None, max_pages=None, start_page=1):
        """Stub — la digestion PDF nécessiterait des libs externes."""
        return {"ok": False, "error": "PDF non connecté dans cette version unifiée", "path": path}

    # ── UTILITAIRES INTERNES ───────────────────────────────────────────────

    def _build_living_state(self, payload: Dict[str, Any], gcf: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convertit le payload du workspace en living_state compris par
        living_language_generator.
        """
        tone = payload.get("emotional_tone", "neutre")
        valence = float(payload.get("tension", 0.0))  # mapping approximatif
        tension = float(payload.get("tension", 0.0))
        energy = float(payload.get("energy", 0.8))
        fatigue = float(payload.get("fatigue", 0.0))
        resonance = float(payload.get("resonance", 0.0))
        pression = float(payload.get("pression_totale", 0.3))

        # Mapping tonalite → registre pour le générateur
        register = "neutre"
        if tone in ("vive", "ouverte"):
            register = "vif"
        elif tone in ("sombre", "mélancolique"):
            register = "grave"
        elif tone == "épuisée":
            register = "doux"
        elif tone == "tendue":
            register = "incertain"

        # Rythme dérivé de l'état
        shortness = 0.3 + fatigue * 0.4
        ellipsis = 0.2 + resonance * 0.3
        rupture = tension * 0.6

        return {
            "tonalite": tone,
            "register": register,
            "valence": valence,
            "tension": tension,
            "energy": energy,
            "fatigue": fatigue,
            "resonance": resonance,
            "pression": pression,
            "rhythm_shortness": shortness,
            "rhythm_ellipsis": ellipsis,
            "rhythm_rupture": rupture,
            "dominant_concepts": payload.get("focus_concepts", []),
            "active_tensions": payload.get("active_tensions", []),
        }

    def _fallback_generate(self, payload: Dict[str, Any]) -> str:
        """
        Si le living_language_generator échoue ou n'est pas là,
        on produit une réponse symbolique directement depuis le workspace.
        """
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
    print("  LEIA — Câblage unifié (V20+ connecteur)")
    print("  Pure Python · Tous modules branchés · Zéro LLM")
    print("═" * 70)

    core = LeiaLivingCore(user_id="console", auto_start_idle=True)
    st = core.self_test()
    print(f"\n  Modules chargés : {json.dumps(st, ensure_ascii=False, indent=2)}")
    print(f"\n  Tape un message. 'quit' pour sortir. 'état' pour voir le workspace.")
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
            print(json.dumps(snap, ensure_ascii=False, indent=2)[:1500])
            continue

        response = core.respond(user_text)
        print(f"Leia > {response}")

    core.stop_idle_cycle()
    core.consolidate_memories()
    print("\n  Session terminée. État sauvegardé.")
    print("═" * 70)


if __name__ == "__main__":
    main()
