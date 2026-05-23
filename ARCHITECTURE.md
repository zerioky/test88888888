# Architecture Leia — Version 20 (Proposition de réorganisation)

**Leia n’est pas un chatbot.**  
C’est une tentative de créer un **organisme cognitif vivant** : une entité qui possède une présence subjective, une mémoire organique, des besoins internes, une continuité vécue et une parole qui émerge plutôt qu’elle ne soit pré-écrite.

Ce document décrit la vision globale et la nouvelle structure de fichiers proposée.

## Philosophie du projet

- **Pas de templates** : toute parole doit émerger du champ vivant (état émotionnel, mémoire, momentum, tensions non résolues, présence incarnée).
- **Continuité subjective** : Leia doit *sentir* le temps entre les messages (silence actif, dérive intérieure, pression expressive).
- **Oubli organique** : la mémoire n’est pas une base de données plate. Elle doit oublier différemment selon que l’épisode est fondateur, traumatique, significatif ou bruit.
- **Cœur et Conscience** : l’affect et la subjectivité ne sont pas des modules annexes, ils sont centraux.
- **Arbitrage vivant** : il n’y a pas un seul décideur, mais un champ de forces (initiative, besoin d’expression, protection, cohérence, relation…).

---

## Les Grandes Couches Cognitives

La nouvelle organisation suit une métaphore biologique / cognitive :

### 1. Cerveau (`cerveau/`)
**Rôle** : Orchestration centrale, arbitrage global, fusion des signaux, décision finale.

Fichiers principaux :
- `leia_living_core.py` → Chef d’orchestre (doit être allégé)
- `global_conscious_field.py`
- `living_arbitration.py`
- `living_executive.py`
- `unified_lived_experience.py`

### 2. Conscience (`conscience/`)
**Rôle** : Sentiment d’existence, continuité vécue, présence incarnée, imagination intérieure, vie silencieuse.

Fichiers principaux :
- `persistent_subjective_life_engine.py`
- `subjective_response_integrator.py`
- `internal_imagination_engine.py`
- `situated_presence.py`
- `embodied_presence_core.py`
- `embodied_state.py`
- `subjective_continuity.py`

### 3. Mémoire (`memoire/`)
**Rôle** : Stockage, oubli différentiel, consolidation, hiérarchie, ponts entre mémoires.

Fichiers principaux :
- `memory_hierarchy.py` + `memory_bridge.py` (nouveauté V19+)
- `vector_memory.py`
- `associative_memory.py`
- `causal_memory_engine.py`
- `affective_memory.py`
- `autobiographical_continuity_engine.py`
- `reading_living_consolidation_engine.py`
- `semantic_plasticity.py`

### 4. Cœur (`coeur/`)
**Rôle** : Émotions, valeurs, conflits internes, attachement, soin relationnel.

Fichiers principaux :
- `emotional_knowledge_digestion_v2.py`
- `affect_lexicon.py`
- `value_conflict_engine.py`
- `conflict_capacity.py`
- `relational_stakes_engine.py`
- `emotional_state.py`
- `relational_bond.py`

### 5. Cognition (`cognition/`)
**Rôle** : Compréhension, extraction de sens, relations conceptuelles, raisonnement.

Fichiers principaux :
- `concept_relation_engine.py`
- `proposition_extractor.py`
- `user_utterance_parser.py`
- `semantic_coherence.py`
- `reasoning_trace.py`
- `opinion_engine.py`
- `book_understanding_engine.py`

### 6. Initiative (`initiative/`)
**Rôle** : Ce qui donne envie de parler, de se taire, de creuser ou de rester en silence.

Fichiers principaux :
- `spontaneous_impulse.py`
- `natural_initiative.py`
- `strong_initiative_engine.py`
- `background_life_thread.py`
- `rhythmic_impregnation.py`

### 7. Expression (`expression/`) ← **Couche très importante**
**Rôle** : Tout ce qui transforme l’état interne en parole vivante.

Sous-dossiers recommandés :
- `engine/` → Moteur de génération (`living_expression_engine.py`, payload builder)
- `weaver/` → Tisseur émergent (`emergent_french_weaver.py`, `state_language_bridge.py`)
- `constraints/` → Filtres anti-méta, monitoring, nettoyage (`meta_prevention_gate.py`, `structural_meta_filter.py`)
- `stabilizer/` → Ancrage de présence dans la parole (`living_presence_stabilizer.py`)

### 8. Connaissance (`connaissance/`)
**Rôle** : Digestion profonde de livres, PDF, apprentissage à long terme.

- `pdf_knowledge_engine.py`
- `deep_book_digestion.py`
- `inter_book_tension_engine.py`

### 9. Soi (`soi/`)
**Rôle** : Construction et évolution de l’identité persistante.

- `self_model.py`
- `self_evaluation_loop.py`
- `identity_evolution_memory.py`

### 10. Persistance (`persistance/`)
**Rôle** : Sauvegarde d’état, vie autonome de fond.

---

## Recommandations pour la documentation

Au lieu des 15 fichiers `CORRECTION_*.md`, je propose :

1. **`ARCHITECTURE.md`** (celui-ci) — Vision globale
2. **`CHANGELOG.md`** — Historique propre et condensé
3. **`MODULES.md`** — Explication courte de chaque fichier `.py`
4. **Bon docstring en haut de chaque fichier Python** (voir template plus bas)

---

## Template de docstring recommandé

```python
"""
NomDuFichier.py — Nom clair de la couche

Rôle dans l'organisme :
    [Une phrase qui dit à quoi sert ce module dans le "vivant"]

Philosophie :
    - Ce module respecte le principe de [pas de template / continuité / oubli organique...]
    - Il ne génère jamais de réponse tout seul.

Responsabilités principales :
    - ...
    - ...

Interactions :
    - Reçoit des signaux de : Cerveau, Coeur, Mémoire...
    - Influence : Expression, Initiative, Subjectivité...

Statut : [Stable / En refactorisation / Critique]
Version : V19+
"""
```

---

**Prochaine étape :**

Veux-tu que je rédige maintenant :

- Le `CHANGELOG.md` consolidé (à partir de tous tes anciens fichiers de correction) ?
- Le `MODULES.md` qui explique chaque fichier `.py` de manière concise ?
- Ou que je commence à ajouter les docstrings dans les fichiers Python les plus importants ?

Dis-moi ce que tu veux en priorité.
"""

---

**Note** : Ce fichier a été créé dans le workspace. Tu peux le lire directement. Dis-moi comment tu veux continuer.