"""conversation_window.py — mémoire courte de conversation.

But : donner à Leia accès aux N derniers échanges réels (texte utilisateur
+ texte Leia), pour qu'elle sache ce qu'elle vient de dire et ce qui a été
demandé il y a 30 secondes.

Ce module ne génère aucune phrase. Il stocke, résout les références, expose
un snapshot utilisable par le contexte de réponse.

Trois fonctions principales :
 1. Stocker chaque échange (user_input + leia_response).
 2. Exposer les N derniers tours pour le contexte de génération.
 3. Résoudre les références pronominales : "ça", "cette question",
    "ce que tu as dit", "ta réponse précédente", etc.
"""
from __future__ import annotations

import json
import os
import re
import time
from collections import deque
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Déclencheurs de référence à la réponse précédente
# ---------------------------------------------------------------------------

_REF_TRIGGERS: List[str] = [
    "ça",
    "ca",
    "cela",
    "cette question",
    "ce que tu as dit",
    "ce que tu viens de dire",
    "ta réponse",
    "ta reponse",
    "ce mot",
    "ce truc",
    "ce point",
    "l'autre chose",
    "ce que tu mentionnes",
    "ce que tu mentionnais",
    "cette idée",
    "cette idee",
    "cette notion",
    "la question que tu gardes",
    "la question que tu as gardée",
]

# Pronoms référentiels qui pointent vers le tour précédent
_REF_PRONOUNS = re.compile(
    r"\b(ça|ca|cela|celle-là|celui-là|celle-ci|celui-ci)\b",
    re.IGNORECASE,
)

def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip().lower()


class ConversationTurn:
    """Un échange unique : ce que l'utilisateur a dit + ce que Leia a répondu."""

    __slots__ = ("user", "leia", "at", "index", "user_atoms", "leia_atoms")

    def __init__(self, user: str, leia: str, index: int) -> None:
        self.user: str = str(user or "")[:400]
        self.leia: str = str(leia or "")[:600]
        self.at: float = time.time()
        self.index: int = index
        # Atomes extraits pour la résolution de références
        self.user_atoms: List[str] = self._atoms(self.user)
        self.leia_atoms: List[str] = self._atoms(self.leia)

    @staticmethod
    def _atoms(text: str) -> List[str]:
        """Extrait les mots significatifs (>3 lettres, non-stop)."""
        stop = {
            "que", "qui", "quoi", "dont", "pour", "par", "dans", "sur", "avec",
            "sans", "vers", "comme", "plus", "moins", "très", "tres", "mais",
            "est", "sont", "être", "etre", "fait", "font", "peut", "doit",
            "le", "la", "les", "un", "une", "des", "du", "de", "ce", "cet",
            "cette", "ces", "son", "sa", "ses", "mon", "ma", "mes",
            "il", "elle", "on", "nous", "vous", "ils", "elles", "je", "tu",
        }
        words = re.findall(r"[a-zà-ÿ]{4,}", _norm(text))
        return [w for w in words if w not in stop]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index,
            "user": self.user,
            "leia": self.leia,
            "at": round(self.at, 2),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConversationTurn":
        t = cls.__new__(cls)
        t.user = str(data.get("user", ""))[:400]
        t.leia = str(data.get("leia", ""))[:600]
        t.at = float(data.get("at", time.time()))
        t.index = int(data.get("index", 0))
        t.user_atoms = cls._atoms(t.user)
        t.leia_atoms = cls._atoms(t.leia)
        return t


class ConversationWindow:
    """Fenêtre courte de mémoire conversationnelle.

    Stocke les N derniers échanges sous forme de ConversationTurn.
    Expose :
    - recent_context(n) : liste des n derniers tours
    - last_leia_said()  : dernier texte produit par Leia
    - resolve_reference(text) : résout les pronoms/expressions déictiques
    - signal_for_context() : dict injecté dans le contexte de génération
    """

    def __init__(
        self,
        maxlen: int = 8,
        storage_path: Optional[str] = None,
    ) -> None:
        self.maxlen = maxlen
        self.storage_path = storage_path
        self._turns: deque[ConversationTurn] = deque(maxlen=maxlen)
        self._total_turns: int = 0
        if storage_path:
            self._load()

    # ------------------------------------------------------------------
    # API principale
    # ------------------------------------------------------------------

    def add_turn(self, user_input: str, leia_response: str) -> None:
        """Enregistre un échange complet."""
        if not user_input and not leia_response:
            return
        turn = ConversationTurn(user_input, leia_response, self._total_turns)
        self._turns.appendleft(turn)
        self._total_turns += 1
        if self.storage_path:
            self._save()

    def recent_context(self, n: int = 4) -> List[Dict[str, Any]]:
        """Retourne les n derniers tours, du plus récent au plus ancien."""
        return [t.to_dict() for t in list(self._turns)[:n]]

    def last_leia_said(self) -> str:
        """Texte exact de la dernière réponse de Leia."""
        if self._turns:
            return self._turns[0].leia
        return ""

    def last_user_said(self) -> str:
        """Texte exact de la dernière entrée utilisateur."""
        if self._turns:
            return self._turns[0].user
        return ""

    def get_last_leia_response(self, offset: int = 0) -> str:
        """Retourne la dernière réponse de Leia (offset=0) ou l'avant-dernière (offset=1).

        CORRECTION : utilisait self.turns (inexistant) au lieu de self._turns,
        et appelait .get("leia") sur un ConversationTurn au lieu de .leia
        """
        turns = list(self._turns)          # ← corrigé : self._turns
        if not turns:
            return ""
        idx = offset                        # _turns[0] = plus récent
        if idx < len(turns):
            return turns[idx].leia         # ← corrigé : .leia (attribut direct)
        return ""

    def turn_count(self) -> int:
        return self._total_turns

    # ------------------------------------------------------------------
    # Résolution de références
    # ------------------------------------------------------------------

    def resolve_reference(self, text: str) -> str:
        """Résout les références déictiques dans text."""
        if not self._turns:
            return text
        lower = _norm(text)

        # Test 1 : déclencheur littéral
        triggered = any(trigger in lower for trigger in _REF_TRIGGERS)

        # Test 2 : pronom référentiel isolé
        if not triggered:
            triggered = bool(_REF_PRONOUNS.search(text)) and len(text.split()) <= 8

        if not triggered:
            return text

        last = self._turns[0]
        leia_fragment = last.leia[:100].rstrip()
        if len(last.leia) > 100:
            leia_fragment += "…"
        user_fragment = last.user[:60].rstrip()
        if len(last.user) > 60:
            user_fragment += "…"

        annotation = (
            f" [réf·tour{last.index}: "
            f"toi→«{user_fragment}» "
            f"moi→«{leia_fragment}»]"
        )
        return text + annotation

    def find_topic_in_history(self, topic_atoms: List[str], depth: int = 4) -> Optional[Dict[str, Any]]:
        """Cherche dans les derniers tours lequel est le plus lié à topic_atoms."""
        if not topic_atoms or not self._turns:
            return None
        best_turn = None
        best_score = 0.0
        for turn in list(self._turns)[:depth]:
            all_atoms = set(turn.user_atoms + turn.leia_atoms)
            overlap = sum(1 for a in topic_atoms if a in all_atoms)
            score = overlap / max(len(topic_atoms), 1)
            if score > best_score:
                best_score = score
                best_turn = turn
        if best_score >= 0.25:
            return best_turn.to_dict()
        return None

    # ------------------------------------------------------------------
    # Signal pour le contexte de génération
    # ------------------------------------------------------------------

    def signal_for_context(self) -> Dict[str, Any]:
        """Dict injecté dans build_living_context() et le weaver."""
        if not self._turns:
            return {
                "available": False,
                "recent_turns": [],
                "last_leia_said": "",
                "last_user_said": "",
                "turn_count": 0,
            }
        return {
            "available": True,
            "recent_turns": self.recent_context(4),
            "last_leia_said": self.last_leia_said()[:300],
            "last_user_said": self.last_user_said()[:200],
            "turn_count": self._total_turns,
        }

    def snapshot(self) -> Dict[str, Any]:
        return self.signal_for_context()

    # ------------------------------------------------------------------
    # Persistance
    # ------------------------------------------------------------------

    def _save(self) -> None:
        if not self.storage_path:
            return
        try:
            os.makedirs(os.path.dirname(self.storage_path) or ".", exist_ok=True)
            data = {
                "total_turns": self._total_turns,
                "turns": [t.to_dict() for t in self._turns],
            }
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass

    def _load(self) -> None:
        if not self.storage_path or not os.path.isfile(self.storage_path):
            return
        try:
            with open(self.storage_path, encoding="utf-8") as f:
                data = json.load(f)
            self._total_turns = int(data.get("total_turns", 0))
            raw_turns = data.get("turns", [])
            loaded = [ConversationTurn.from_dict(d) for d in raw_turns[:self.maxlen]]
            self._turns = deque(loaded, maxlen=self.maxlen)
        except Exception:
            pass
