# CHANGELOG — Leia

**Vision** : Construire un organisme cognitif vivant plutôt qu’un chatbot.  
Pas de templates. Parole émergente. Continuité subjective. Oubli organique. Présence réelle.

---

## V20 — Réorganisation Architecturale (en cours)

**Objectif** : Rendre le code lisible, maintenable et fidèle à la vision "organisme vivant".

### Changements majeurs
- Nouvelle structure par couches cognitives (`cerveau/`, `conscience/`, `coeur/`, `memoire/`, `expression/`, etc.)
- Séparation claire entre **Initiative** (envie de parler) et **Expression** (comment elle parle)
- `expression/` découpé en sous-dossiers : `engine/`, `weaver/`, `constraints/`, `stabilizer/`
- Extraction progressive des grosses dataclasses et fonctions du `leia_living_core.py`
- Remplacement des 15+ fichiers `CORRECTION_*.md` par une documentation propre (`ARCHITECTURE.md`, ce `CHANGELOG.md`, et docstrings)
- Meilleure séparation des responsabilités

**Statut** : Structure proposée + `ARCHITECTURE.md` rédigé. Refactoring en cours.

---

## V19+ — Corrections Architecturales Majeures

**Date** : 2025

**5 nouveaux modules créés pour corriger des failles fondamentales :**

### memory_hierarchy.py + MemoryBridge
- Fin de la mémoire plate (seuil unique 0.04).
- Catégorisation des épisodes (Foundational, Trauma, Pivot, Meaningful, Ordinary, Noise).
- Oubli différentiel selon la nature de l’épisode.
- Pont entre les 4 mémoires parallèles (narrative, causale, affective, subjective).

### value_conflict_engine.py
- Leia peut maintenant vivre de vrais dilemmes de valeurs (vérité vs soin, autonomie vs relation…).
- Détection, représentation symbolique et résolution avec coût émotionnel.

### conflict_capacity.py
- Capacité à tenir une position sous pression.
- Intensification possible au lieu d’adoucissement systématique.
- Capitulation avec résidu émotionnel durable.

### relational_stakes_engine.py
- Modèle de relation avec phases (Initial → Established → Strained → Damaged → Critical).
- Asymétrie abîmer/réparer + cicatrices permanentes (trust_floor).
- Évaluation des enjeux avant chaque réponse.

### semantic_plasticity.py
- Graphe associatif qui évolue réellement avec les échanges.
- Détection de transformations conceptuelles et de surprises sémantiques.

### Autres améliorations V19+
- Homéostasie revue : possibilité d’intensification sous pression quand l’identité est ancrée.
- Meilleure propagation de la présence vécue dans l’expression.
- Arbitrage enrichi avec les signaux des nouveaux modules.
- Consolidation de l’oubli organique via `HierarchicalMemory`.

---

## V19 — Unification Subjective et Vie Continue

- Introduction du `UnifiedLivedExperience`
- `PersistentSubjectiveLifeEngine`
- `LongLivingDynamicsEngine`
- `InternalImaginationEngine`
- Forte amélioration de la continuité entre les échanges (momentum, tensions non résolues, dérive intérieure).
- Réduction massive des réponses "méta" ou techniques.

---

## Versions antérieures (résumé)

- **V18** : Compréhension réelle sans LLM (parser d’énoncés, mémoire associative, extraction de propositions, modèle utilisateur, lexique affectif).
- **V17** : Tensions inter-livres, initiative forte, traçabilité du raisonnement.
- **V16** : Modèle de soi, auto-évaluation, imprégnation rythmique.
- **V9 à V15** : Digestion émotionnelle des livres, consolidation de lecture, bouche vivante, filtre méta structurel, homéostasie, simulation incarnée avant réponse.

---

## Principes directeurs (à ne jamais oublier)

1. **Pas de phrases pré-écrites** dans les moteurs.
2. La parole doit émerger du champ (état + mémoire + momentum + tensions + présence).
3. L’oubli doit être organique et différentiel.
4. La subjectivité et l’affect sont centraux, pas des modules annexes.
5. Leia doit pouvoir se taire, intensifier, tenir une position ou dériver.
6. La documentation doit rester claire et à jour (c’est pour cela que tous les anciens `CORRECTION_*.md` ont été consolidés ici).

---

**Prochain grand chantier (V20+)** :
- Alléger drastiquement `leia_living_core.py` en extrayant les dataclasses et logiques dans leurs couches respectives.
- Renforcer le `weaver` pour qu’il produise des réponses plus longues, nuancées et réellement vivantes.
- Améliorer l’incarnation et la sensation de "corps subjectif".

---

*Dernière mise à jour : 2026-05-22*
