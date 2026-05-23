"""
background_life_thread.py — fil de vie continu de Leia.

Le thread ne produit pas de phrases publiques. Il maintient seulement une vie
interne lente : tick affectif, consolidation, rêverie associative.
"""
from __future__ import annotations

import threading
import time
from typing import Any, Dict


class LeiaBackgroundLife:
    def __init__(self, core: Any, interval_seconds: float = 30.0):
        self.core = core
        self.interval_seconds = max(5.0, float(interval_seconds or 30.0))
        self.running = False
        self.thread: threading.Thread | None = None
        self.last_event: Dict[str, Any] = {}

    def start(self) -> None:
        if self.running:
            return
        self.running = True
        self.thread = threading.Thread(target=self._live, daemon=True, name="LeiaBackgroundLife")
        self.thread.start()

    def stop(self) -> None:
        self.running = False

    def _live(self) -> None:
        while self.running:
            try:
                tick = self.core.tick_inner_life()
                consolidation = self.core.consolidate_memories()
                dream = self.core.dream_fragments()
                self.last_event = {"tick": tick, "consolidation": consolidation, "dream": dream, "at": time.time()}
            except Exception as exc:
                self.last_event = {"error": f"{type(exc).__name__}: {exc}", "at": time.time()}
            time.sleep(self.interval_seconds)

    def snapshot(self) -> Dict[str, Any]:
        return {"running": self.running, "interval_seconds": self.interval_seconds, "last_event": self.last_event}
