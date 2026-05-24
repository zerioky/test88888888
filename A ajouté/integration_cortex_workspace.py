#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
integration_cortex_workspace.py
═══════════════════════════════════════════════════════════════════════════════
Le workspace ne reçoit PLUS de concepts pré-mâchés.
Il reçoit des structures cognitives du SemanticCortex.

Pipeline :
  Texte brut → SemanticCortex → CognitiveStructure
     ↓
  Workspace.ingest_structure(structure)
     ↓
  Causal links → graphe causal vivant
  Tensions → émergences dialectiques
  Abstractions → méta-concepts auto-générés
  Scènes → pensées actives situationnelles
  Propagation associative profonde
"""

import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from semantic_cortex import SemanticCortex, CognitiveStructure, CausalLink, DialecticalTension, AbstractionEdge
from global_workspace_v2 import GlobalWorkspace, PenseeActive, workspace

print("═" * 70)
print("  INTÉGRATION CORTEX ↔ WORKSPACE V2")
print("  Le workspace comprend par lui-même. Zéro concepts pré-mâchés.")
print("═" * 70)


class CognitiveWorkspace(GlobalWorkspace):
    """
    Workspace enrichi qui ingère des CognitiveStructure complètes
    au lieu de signaux pré-digérés.
    """

    def ingest_structure(self, cs: CognitiveStructure, source: str = "") -> None:
        """
        Ingère une structure cognitive complète.
        Le workspace ANALYSE, ne reçoit pas.
        """
        if not cs or not cs.raw:
            return

        self._n_perceptions += 1
        self._derniere_activite = time.time()

        # ── 1. Concepts extraits par le CORTEX, pas donnés ───────────────
        concepts = cs.concepts[:10]
        if concepts:
            activations = self.propagation.propager(
                concepts, force_initiale=0.5 + cs.emotional_arousal * 0.3, profondeur=3
            )
            # Les concepts du cortex deviennent attracteurs si émotion forts
            for c, f in sorted(activations.items(), key=lambda x: -x[1])[:4]:
                if f > 0.4:
                    self.propagation.renforcer_attracteur(c, f * 0.25)

            if concepts:
                self.attention.orienter(concepts[0], force=0.7)
                voisins = []
                for c in concepts[:2]:
                    voisins.extend(self.propagation.voisins_actifs(c, n=2))
                self.attention.ajouter_secondaire(list(dict.fromkeys(voisins))[:3])

        # ── 2. CAUSALITÉ → graphe causal vivant ──────────────────────────
        for cl in cs.causal_links:
            self._integrate_causal(cl)

        # ── 3. TENSIONS DIALECTIQUES → émergences ────────────────────────
        for dt in cs.tensions:
            self._integrate_tension(dt)

        # ── 4. ABSTRACTIONS → méta-concepts ─────────────────────────────
        for ab in cs.abstractions:
            self._integrate_abstraction(ab)

        # ── 5. SCÈNES → pensées situationnelles ───────────────────────────
        for scene in cs.scenes:
            if scene.sujet or scene.action:
                self._create_scene_thought(scene, source)

        # ── 6. Contamination émotionnelle (de la structure, pas du signal)
        self.champ_emotionnel.contaminer(
            valence=cs.emotional_valence,
            arousal=cs.emotional_arousal,
            tension=len(cs.tensions) * 0.15 + len(cs.causal_links) * 0.05,
            force=0.3 + cs.emotional_arousal * 0.2,
        )

        # ── 7. Pression expressive ───────────────────────────────────────
        if cs.is_question:
            self.pression.augmenter("curiosite", 0.25 + cs.emotional_arousal * 0.2)
        if cs.tensions:
            self.pression.augmenter("tension", len(cs.tensions) * 0.15)
        if cs.causal_links:
            self.pression.augmenter("concept", len(cs.causal_links) * 0.08)
        self.pression.augmenter("momentum", cs.complexity * 0.1)

        # ── 8. Monologue ─────────────────────────────────────────────────
        self.monologue.noter(
            "perception_structurelle",
            concepts[:5],
            intensite=0.4 + abs(cs.emotional_valence) * 0.3,
            source=source or cs.source,
        )
        if cs.is_question:
            self.monologue.ajouter_question(f"{concepts[0] if concepts else '?'} ?")

        # ── 9. Apprentissage liens co-occurrence ────────────────────────
        for i in range(len(concepts)):
            for j in range(i + 1, min(len(concepts), i + 3)):
                self.propagation.apprendre_lien(concepts[i], concepts[j], force=0.25)

        # ── 10. Auto-émergence : si forte tension + causalité, pensée méta ─
        if cs.tensions and cs.causal_links:
            self._emergence_meta_cognitive(cs)

    def _integrate_causal(self, cl: CausalLink) -> None:
        """Un lien causal devient une pensée active de type 'inférence'."""
        pensee = self._creer_pensee(
            id=self._nouveau_id(),
            contenu=f"cause:{cl.cause[:30]}→{cl.effect[:30]}",
            concepts=[cl.cause, cl.effect, cl.trigger],
            poids=cl.force * 0.8,
            charge=0.0,
            tension=0.2 if cl.direction == "⊣" else 0.0,
            source="causal_inference",
            persistante=(cl.force > 0.75),
        )
        pensee.attracteur = True
        pensee.poids_attracteur = cl.force * 0.3
        self._ajouter_pensee(pensee)

        # Le lien causal enrichit le réseau associatif avec un TYPE
        self.propagation.apprendre_lien(cl.cause, cl.effect, force=cl.force)

        # Si c'est une inhibition → tension conceptuelle implicite
        if cl.direction == "⊣":
            self.propagation.apprendre_lien(cl.cause, "_inhibition_" + cl.effect, force=cl.force * 0.5)

    def _integrate_tension(self, dt: DialecticalTension) -> None:
        """Une tension dialectique crée une pensée conflictuelle active."""
        pensee = self._creer_pensee(
            id=self._nouveau_id(),
            contenu=f"tension:{dt.these[:25]}↔{dt.antithese[:25]}",
            concepts=[dt.these, dt.antithese, dt.type_tension],
            poids=dt.force * 0.9,
            tension=dt.force,
            source="dialectical_emergence",
            persistante=True,
        )
        pensee.attracteur = True
        pensee.poids_attracteur = dt.force * 0.4
        self._ajouter_pensee(pensee)

        # La tension devient attracteur des deux pôles
        self.propagation.renforcer_attracteur(dt.these, dt.force * 0.2)
        self.propagation.renforcer_attracteur(dt.antithese, dt.force * 0.2)

        # Émergence : pensée sur la résolution
        self._creer_pensee_interne(
            f"resolver:{dt.these[:20]}_{dt.antithese[:20]}",
            [dt.these, dt.antithese, "résolution", "synthèse"],
            poids=dt.force * 0.3,
            tension=dt.force * 0.5,
        )

    def _integrate_abstraction(self, ab: AbstractionEdge) -> None:
        """Une abstraction crée un méta-concept attracteur."""
        # Le concept général devient attracteur
        self.propagation.renforcer_attracteur(ab.general, ab.force * 0.3)
        self.propagation.apprendre_lien(ab.specifique, ab.general, force=ab.force, bidirectionnel=False)

        # Pensée de niveau méta
        pensee = self._creer_pensee(
            id=self._nouveau_id(),
            contenu=f"meta:{ab.specifique[:25]}→{ab.general[:25]}",
            concepts=[ab.specifique, ab.general, ab.type_abstraction],
            poids=ab.force * 0.6,
            source="abstraction",
            attracteur=True,
        )
        pensee.poids_attracteur = ab.force * 0.25
        self._ajouter_pensee(pensee)

        # Si abstraction forte, question flottante sur le lien
        if ab.force > 0.7:
            self.monologue.ajouter_question(
                f"Pourquoi {ab.specifique} est-il {ab.type_abstraction} de {ab.general} ?"
            )

    def _create_scene_thought(self, scene, source: str) -> None:
        """Une scène mentale devient une pensée situationnelle."""
        contenu = f"scene:{scene.sujet or '?'}:{scene.action or '?'}:{scene.objet or '?'}"
        pensee = self._creer_pensee(
            id=self._nouveau_id(),
            contenu=contenu[:70],
            concepts=[scene.sujet, scene.action, scene.objet, scene.but, scene.lieu],
            poids=0.4 + abs(scene.emotional_valence) * 0.3,
            charge=scene.emotional_valence,
            source="scene",
        )
        self._ajouter_pensee(pensee)

    def _emergence_meta_cognitive(self, cs: CognitiveStructure) -> None:
        """Émergence de niveau méta : le système pense à sa propre compréhension."""
        top_concept = cs.concepts[0] if cs.concepts else "?"
        self._creer_pensee_interne(
            f"meta:je_comprends_{top_concept}",
            [top_concept, "compréhension", "structure", "sens"],
            poids=0.25,
            attracteur=True,
        )
        self.monologue.noter(
            "meta_cognition", [top_concept, "compréhension"],
            intensite=0.3, source="auto_emergence"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# TEST INTÉGRÉ
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import time

    cortex = SemanticCortex()
    ws = CognitiveWorkspace()

    phrases = [
        "Parce que la liberté suppose la contrainte, l'existence individuelle est une tension permanente.",
        "Je ne suis pas d'accord : la mémoire n'est pas un tiroir, mais une durée vécue.",
        "Si l'intelligence artificielle efface l'essentiel en nous, alors l'humanité perdra sa continuité.",
        "Bergson affirme que la durée est irréductible à l'espace, ce qui signifie que le temps vécu ne se mesure pas.",
    ]

    for i, phrase in enumerate(phrases, 1):
        print(f"\n{'─' * 70}")
        print(f"  [TOUR {i}] Texte brut : {phrase[:65]}")
        print("─" * 70)

        # Le CORTEX comprend
        struct = cortex.process(phrase)
        print(f"  Cortex a trouvé : {struct.to_dict()['n_causal']} causalités, "
              f"{struct.to_dict()['n_tensions']} tensions, "
              f"{struct.to_dict()['n_abstractions']} abstractions")

        # Le WORKSPACE ingère la STRUCTURE
        ws.ingest_structure(struct, source=f"tour_{i}")

        # Lecture de l'état vivant
        dom = ws.pensee_dominante()
        emotion = ws.champ_emotionnel.snapshot()
        tensions = ws.tensions_actives()
        profondeurs = ws.monologue.profondeurs(4)
        attracteurs = list(ws.propagation._attracteurs.keys())[:5]

        print(f"\n  [WORKSPACE]")
        print(f"    Dominante       : {dom.contenu[:55] if dom else '-'} (score={round(dom.score_attention(emotion['valence'], emotion['tension']), 3) if dom else 0})")
        print(f"    Tonalité        : {emotion['tonalite']} | valence={emotion['valence']:+.3f}")
        print(f"    Tensions actives: {[(a, b) for a, b, _ in tensions[:2]]}")
        print(f"    Attracteurs     : {attracteurs}")
        print(f"    Profondeurs     : {profondeurs}")
        print(f"    Pression        : {ws.pression.total():.3f}")

        # Tick de fond
        ws.tick(elapsed=3.0)

    # État final
    print(f"\n{'═' * 70}")
    print("  ÉTAT FINAL (après 4 structures + ticks)")
    print("═" * 70)
    snap = ws.snapshot()
    print(f"\n  Pensées actives   : {len(ws.pensees_actives())}")
    print(f"  Attracteurs vivants: {list(ws.propagation._attracteurs.keys())[:6]}")
    print(f"  Ruminations       : {ws.ruminations_actives()[:2]}")
    print(f"  Questions flott.  : {ws.monologue.questions_flottantes[:3]}")
    print(f"  Tonalité globale  : {ws.champ_emotionnel.tonalite()}")

    # Payload pour expression
    pl = ws.payload_pour_expression()
    print(f"\n  Payload dominant    : {pl['dominant_thought'][:50]}")
    print(f"  Active tensions     : {pl['active_tensions']}")
    print(f"  Profondeurs         : {pl.get('profondeurs', [])}")
    print(f"  Cycles cognitive    : {pl['cycle_count']}")

    print(f"\n{'═' * 70}")
    print("  Le workspace COMPREND par structures. Plus de concepts donnés.")
    print("═" * 70)
