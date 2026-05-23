"""
leia_book_patch.py
-------------------
Patch automatique de LeiaLivingCore pour injecter les données
de livre dans le payload d'expression.

À importer UNE FOIS dans run_leia_ui.py après les imports principaux.
"""
from __future__ import annotations
import sys, os

def apply_book_payload_patch():
    """
    Patche LeiaLivingCore._build_living_expression_payload pour que
    les concepts des livres lus soient toujours injectés dans le payload
    envoyé au weaver, même si leia_living_core ne le fait pas nativement.
    """
    try:
        from leia_living_core import LeiaLivingCore
    except Exception as e:
        print(f"[PATCH] Impossible d'importer LeiaLivingCore: {e}")
        return False

    try:
        from state_language_bridge_patch import enrich_payload_with_book
    except Exception as e:
        print(f"[PATCH] Impossible d'importer enrich_payload_with_book: {e}")
        return False

    # Récupère la méthode originale
    original_method = getattr(LeiaLivingCore, "_build_living_expression_payload", None)
    if original_method is None:
        print("[PATCH] _build_living_expression_payload introuvable dans LeiaLivingCore")
        return False

    # Crée la version patchée
    def _patched_build_living_expression_payload(self, user_input, context):
        # Appelle la méthode originale
        payload = original_method(self, user_input, context)

        # Enrichit avec les données de livre
        if isinstance(payload, dict) and hasattr(self, "living_state"):
            payload = enrich_payload_with_book(payload, self.living_state)

        return payload

    # Applique le patch
    LeiaLivingCore._build_living_expression_payload = _patched_build_living_expression_payload
    print("[PATCH] ✓ Injection des données de livre dans le payload activée")
    return True


# Applique automatiquement au import
apply_book_payload_patch()
