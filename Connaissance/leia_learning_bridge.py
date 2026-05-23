# leia_learning_bridge.py
# Project Leia / project_leia
#
# Connecteur propre:
# emotional_knowledge_digestion_v2
# -> mémoire
# -> spontaneous impulse engine
# -> state/language payload
#
# Ce fichier ne contient aucune phrase préécrite.
# Il transporte uniquement des états, pressions, concepts et attracteurs.

from __future__ import annotations

from typing import Any, Dict, Optional

from emotional_knowledge_digestion_v2 import EmotionalKnowledgeDigestion


class LeiaLearningBridge:
    def __init__(
        self,
        memory_system: Optional[Any] = None,
        impulse_engine: Optional[Any] = None,
        storage_dir: str = "data/digestion_memory",
    ) -> None:
        self.memory_system = memory_system
        self.impulse_engine = impulse_engine
        self.digestion = EmotionalKnowledgeDigestion(
            memory_system=memory_system,
            storage_dir=storage_dir,
        )

    def digest_text(
        self,
        text: str,
        source: str = "unknown_source",
        leia_state: Optional[Dict[str, Any]] = None,
    ):
        self.digestion.set_leia_state(leia_state or {})
        return self.digestion.digest_text(text, source=source)

    def digest_pdf(
        self,
        pdf_path: str,
        source: Optional[str] = None,
        leia_state: Optional[Dict[str, Any]] = None,
    ):
        self.digestion.set_leia_state(leia_state or {})
        return self.digestion.digest_pdf(pdf_path, source=source)

    def enrich_payload_before_language(
        self,
        payload: Dict[str, Any],
        user_text: str,
        leia_state: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        enriched = self.digestion.integrate_with_state_language_payload(
            payload=payload,
            context_text=user_text,
            leia_state=leia_state,
        )

        if self.impulse_engine is not None:
            self.digestion.integrate_with_impulse_engine(
                self.impulse_engine,
                context_text=user_text,
                leia_state=leia_state,
            )

        return enriched

    def tick(self, elapsed_seconds: float = 1.0) -> None:
        self.digestion.tick(elapsed_seconds)
