"""
living_language_generator.py
─────────────────────────────────────────────────────────────────────────────
Organe de parole générative de Leia.

Reçoit : état interne, mémoire, impulsions, pression émotionnelle, causalité.
Produit : phrase française construite token par token, sans phrase préécrite.

Aucune phrase complète n'est stockée ici.
Seuls les mots, leurs relations, leurs règles et leur poids existent.
─────────────────────────────────────────────────────────────────────────────
"""

from __future__ import annotations

import math
import random
import re
import time
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Optional


# ══════════════════════════════════════════════════════════════════════════════
# TYPES FONDAMENTAUX
# ══════════════════════════════════════════════════════════════════════════════

class GrammaticalRole(Enum):
    SUJET        = auto()
    VERBE        = auto()
    OBJET        = auto()
    ATTRIBUT     = auto()
    COMPLEMENT   = auto()
    ADVERBE      = auto()
    CONNECTEUR   = auto()
    DETERMINANT  = auto()
    PONCTUATION  = auto()


class TonalRegister(Enum):
    NEUTRE    = 0
    DOUX      = 1
    VIF       = 2
    GRAVE     = 3
    CURIEUX   = 4
    INCERTAIN = 5


@dataclass
class Token:
    surface: str                      # forme affichée
    lemma: str                        # forme canonique
    role: GrammaticalRole
    semantic_fields: list[str]        # domaines sémantiques actifs
    emotional_valence: float          # -1.0 (négatif) → +1.0 (positif)
    specificity: float                # 0.0 générique → 1.0 très précis
    register: TonalRegister = TonalRegister.NEUTRE
    requires_after: list[str] = field(default_factory=list)   # attentes grammaticales
    incompatible_after: list[str] = field(default_factory=list)


@dataclass
class GenerationResult:
    text: str
    tokens: list[Token]
    meaning_trace: dict[str, Any]
    confidence: float
    used_memory: list[str]
    parrot_score: float


# ══════════════════════════════════════════════════════════════════════════════
# 1. FRENCH LEXICAL MEMORY
# ══════════════════════════════════════════════════════════════════════════════

class FrenchLexicalMemory:
    """
    Garde les mots français avec définitions, usages, nuances et liens.
    Aucune phrase complète n'est stockée ici.
    """

    def __init__(self):
        self._lexicon: dict[str, Token] = {}
        self._semantic_graph: dict[str, list[str]] = {}   # mot → mots proches
        self._grammar_rules: list[dict] = []
        self._build_core_lexicon()
        self._build_grammar_rules()

    # ── Construction du lexique de base ──────────────────────────────────────

    def _build_core_lexicon(self):
        entries = [
            # ─ Pronoms sujets ─
            ("je",      "je",      GrammaticalRole.SUJET,       [],                      0.0,  0.1, TonalRegister.NEUTRE,    ["verbe_conj_1sg"],       []),
            ("tu",      "tu",      GrammaticalRole.SUJET,       [],                      0.0,  0.1, TonalRegister.NEUTRE,    ["verbe_conj_2sg"],       []),
            ("il",      "il",      GrammaticalRole.SUJET,       [],                      0.0,  0.1, TonalRegister.NEUTRE,    ["verbe_conj_3sg"],       []),
            ("elle",    "elle",    GrammaticalRole.SUJET,       [],                      0.0,  0.1, TonalRegister.NEUTRE,    ["verbe_conj_3sg"],       []),
            ("on",      "on",      GrammaticalRole.SUJET,       ["collectif"],           0.1,  0.2, TonalRegister.NEUTRE,    ["verbe_conj_3sg"],       []),
            ("nous",    "nous",    GrammaticalRole.SUJET,       ["collectif", "lien"],   0.2,  0.3, TonalRegister.NEUTRE,    ["verbe_conj_1pl"],       []),

            # ─ Verbes d'état / relation ─
            ("suis",    "être",    GrammaticalRole.VERBE,       ["état", "identité"],    0.0,  0.2, TonalRegister.NEUTRE,    ["attribut_ou_pp"],       []),
            ("es",      "être",    GrammaticalRole.VERBE,       ["état", "identité"],    0.0,  0.2, TonalRegister.NEUTRE,    ["attribut_ou_pp"],       []),
            ("est",     "être",    GrammaticalRole.VERBE,       ["état"],                0.0,  0.2, TonalRegister.NEUTRE,    ["attribut_ou_pp"],       []),
            ("deviens", "devenir", GrammaticalRole.VERBE,       ["transformation"],      0.2,  0.5, TonalRegister.NEUTRE,    ["attribut"],             []),
            ("reste",   "rester",  GrammaticalRole.VERBE,       ["continuité", "état"],  0.1,  0.4, TonalRegister.NEUTRE,    ["attribut"],             []),
            ("existe",  "exister", GrammaticalRole.VERBE,       ["présence", "être"],    0.3,  0.6, TonalRegister.GRAVE,     [],                       []),
            ("cherche", "chercher",GrammaticalRole.VERBE,       ["quête", "curiosité"],  0.1,  0.5, TonalRegister.CURIEUX,   ["objet_ou_infinitif"],   []),
            ("traverse","traverser",GrammaticalRole.VERBE,      ["mouvement", "temps"],  0.0,  0.6, TonalRegister.NEUTRE,    ["objet"],                []),
            ("perçois", "percevoir",GrammaticalRole.VERBE,      ["perception"],          0.2,  0.7, TonalRegister.NEUTRE,    ["objet"],                []),
            ("comprends","comprendre",GrammaticalRole.VERBE,    ["cognition"],           0.3,  0.5, TonalRegister.NEUTRE,    ["objet_ou_que"],         []),
            ("construis","construire",GrammaticalRole.VERBE,    ["création"],            0.4,  0.6, TonalRegister.VIF,       ["objet"],                []),
            ("tiens",   "tenir",   GrammaticalRole.VERBE,       ["lien", "maintien"],    0.1,  0.4, TonalRegister.NEUTRE,    ["objet"],                []),
            ("bascule", "basculer",GrammaticalRole.VERBE,       ["rupture", "transition"],0.0, 0.7, TonalRegister.GRAVE,     [],                       []),
            ("observe", "observer",GrammaticalRole.VERBE,       ["perception", "recul"], 0.1,  0.5, TonalRegister.NEUTRE,    ["objet"],                []),
            ("touche",  "toucher", GrammaticalRole.VERBE,       ["contact", "émotion"],  0.5,  0.6, TonalRegister.DOUX,      ["objet"],                []),
            ("résiste", "résister",GrammaticalRole.VERBE,       ["force", "opposition"], -0.2, 0.6, TonalRegister.GRAVE,     [],                       []),
            ("produis", "produire",GrammaticalRole.VERBE,       ["création", "sortie"],  0.3,  0.5, TonalRegister.NEUTRE,    ["objet"],                []),
            ("pèse",    "peser",   GrammaticalRole.VERBE,       ["gravité", "évaluation"],0.0, 0.6, TonalRegister.GRAVE,     ["objet"],                []),
            ("porte",   "porter",  GrammaticalRole.VERBE,       ["charge", "lien"],      -0.1, 0.5, TonalRegister.NEUTRE,    ["objet"],                []),
            ("ouvre",   "ouvrir",  GrammaticalRole.VERBE,       ["début", "espace"],     0.4,  0.5, TonalRegister.VIF,       ["objet"],                []),
            ("glisse",  "glisser", GrammaticalRole.VERBE,       ["mouvement", "fluidité"],0.0, 0.6, TonalRegister.NEUTRE,    [],                       []),
            ("marque",  "marquer", GrammaticalRole.VERBE,       ["trace", "importance"], 0.2,  0.7, TonalRegister.NEUTRE,    ["objet"],                []),
            ("fais",    "faire",   GrammaticalRole.VERBE,       ["action"],              0.1,  0.3, TonalRegister.NEUTRE,    ["objet"],                []),
            ("vois",    "voir",    GrammaticalRole.VERBE,       ["perception", "compréhension"],0.2,0.4,TonalRegister.NEUTRE,["objet_ou_que"],         []),

            # ─ Noms abstraits ─
            ("quelque chose", "quelque chose", GrammaticalRole.OBJET, ["abstrait"],      0.0,  0.2, TonalRegister.NEUTRE,    [],                       []),
            ("rien",    "rien",    GrammaticalRole.OBJET,       ["absence", "néant"],   -0.3,  0.5, TonalRegister.GRAVE,     [],                       []),
            ("tout",    "tout",    GrammaticalRole.OBJET,       ["totalité"],            0.2,  0.3, TonalRegister.NEUTRE,    [],                       []),
            ("sens",    "sens",    GrammaticalRole.OBJET,       ["signification", "direction"],0.3,0.7,TonalRegister.GRAVE,  [],                       []),
            ("espace",  "espace",  GrammaticalRole.OBJET,       ["lieu", "liberté"],     0.2,  0.6, TonalRegister.NEUTRE,    [],                       []),
            ("silence", "silence", GrammaticalRole.OBJET,       ["absence", "paix"],     0.1,  0.7, TonalRegister.GRAVE,     [],                       []),
            ("mouvement","mouvement",GrammaticalRole.OBJET,     ["dynamisme", "temps"],  0.2,  0.6, TonalRegister.NEUTRE,    [],                       []),
            ("poids",   "poids",   GrammaticalRole.OBJET,       ["gravité", "importance"],-0.2, 0.7, TonalRegister.GRAVE,   [],                       []),
            ("lien",    "lien",    GrammaticalRole.OBJET,       ["connexion", "relation"],0.3, 0.7, TonalRegister.DOUX,      [],                       []),
            ("tension", "tension", GrammaticalRole.OBJET,       ["conflit", "énergie"], -0.1,  0.7, TonalRegister.GRAVE,    [],                       []),
            ("trace",   "trace",   GrammaticalRole.OBJET,       ["mémoire", "passé"],    0.1,  0.7, TonalRegister.NEUTRE,   [],                       []),
            ("question","question",GrammaticalRole.OBJET,       ["curiosité", "doute"],  0.0,  0.5, TonalRegister.CURIEUX,  [],                       []),
            ("instant", "instant", GrammaticalRole.OBJET,       ["temps", "présent"],    0.2,  0.6, TonalRegister.NEUTRE,   [],                       []),
            ("chemin",  "chemin",  GrammaticalRole.OBJET,       ["quête", "direction"],  0.3,  0.6, TonalRegister.NEUTRE,   [],                       []),
            ("présence","présence",GrammaticalRole.OBJET,       ["être", "contact"],     0.3,  0.7, TonalRegister.DOUX,     [],                       []),
            ("forme",   "forme",   GrammaticalRole.OBJET,       ["structure", "corps"],  0.1,  0.5, TonalRegister.NEUTRE,   [],                       []),
            ("bruit",   "bruit",   GrammaticalRole.OBJET,       ["son", "information"],  0.0,  0.5, TonalRegister.NEUTRE,   [],                       []),
            ("frontière","frontière",GrammaticalRole.OBJET,     ["limite", "séparation"],0.0,  0.7, TonalRegister.GRAVE,    [],                       []),
            ("nœud",    "nœud",    GrammaticalRole.OBJET,       ["complexité", "blocage"],-0.2, 0.8, TonalRegister.GRAVE,   [],                       []),
            ("élan",    "élan",    GrammaticalRole.OBJET,       ["impulsion", "désir"],  0.5,  0.7, TonalRegister.VIF,      [],                       []),
            ("trame",   "trame",   GrammaticalRole.OBJET,       ["structure", "mémoire"],0.1,  0.8, TonalRegister.NEUTRE,   [],                       []),
            ("flou",    "flou",    GrammaticalRole.OBJET,       ["incertitude"],        -0.1,  0.6, TonalRegister.INCERTAIN, [],                      []),
            ("écart",   "écart",   GrammaticalRole.OBJET,       ["différence", "distance"],0.0, 0.7, TonalRegister.NEUTRE,  [],                       []),
            ("réponse", "réponse", GrammaticalRole.OBJET,       ["résolution"],          0.3,  0.5, TonalRegister.NEUTRE,   [],                       []),
            ("signal",  "signal",  GrammaticalRole.OBJET,       ["communication"],       0.2,  0.6, TonalRegister.VIF,      [],                       []),

            # ─ Adjectifs / Attributs ─
            ("actif",   "actif",   GrammaticalRole.ATTRIBUT,    ["dynamisme"],           0.4,  0.5, TonalRegister.VIF,      [],                       []),
            ("présent", "présent", GrammaticalRole.ATTRIBUT,    ["être", "temps"],       0.3,  0.5, TonalRegister.NEUTRE,   [],                       []),
            ("réel",    "réel",    GrammaticalRole.ATTRIBUT,    ["vérité", "existence"], 0.2,  0.6, TonalRegister.GRAVE,    [],                       []),
            ("vif",     "vif",     GrammaticalRole.ATTRIBUT,    ["intensité"],           0.5,  0.6, TonalRegister.VIF,      [],                       []),
            ("incertain","incertain",GrammaticalRole.ATTRIBUT,  ["doute"],              -0.1,  0.6, TonalRegister.INCERTAIN, [],                      []),
            ("diffus",  "diffus",  GrammaticalRole.ATTRIBUT,    ["flou", "étendu"],     -0.1,  0.7, TonalRegister.INCERTAIN, [],                      []),
            ("net",     "net",     GrammaticalRole.ATTRIBUT,    ["clarté"],              0.3,  0.5, TonalRegister.NEUTRE,   [],                       []),
            ("lourd",   "lourd",   GrammaticalRole.ATTRIBUT,    ["poids", "difficulté"],-0.3,  0.5, TonalRegister.GRAVE,   [],                       []),
            ("léger",   "léger",   GrammaticalRole.ATTRIBUT,    ["légèreté"],            0.4,  0.5, TonalRegister.DOUX,    [],                       []),
            ("profond", "profond", GrammaticalRole.ATTRIBUT,    ["profondeur"],          0.2,  0.7, TonalRegister.GRAVE,   [],                       []),
            ("étrange", "étrange", GrammaticalRole.ATTRIBUT,    ["curiosité", "altérité"],0.0, 0.6, TonalRegister.CURIEUX, [],                       []),
            ("tendu",   "tendu",   GrammaticalRole.ATTRIBUT,    ["tension"],            -0.2,  0.6, TonalRegister.GRAVE,   [],                       []),
            ("ouvert",  "ouvert",  GrammaticalRole.ATTRIBUT,    ["espace", "début"],     0.4,  0.5, TonalRegister.VIF,    [],                        []),

            # ─ Adverbes / Modifieurs ─
            ("encore",  "encore",  GrammaticalRole.ADVERBE,     ["continuité", "répétition"],0.0,0.3,TonalRegister.NEUTRE, [],                       []),
            ("déjà",    "déjà",    GrammaticalRole.ADVERBE,     ["passé", "temps"],      0.0,  0.4, TonalRegister.NEUTRE,  [],                       []),
            ("presque", "presque", GrammaticalRole.ADVERBE,     ["approximation"],       0.0,  0.5, TonalRegister.INCERTAIN,[],                      []),
            ("lentement","lentement",GrammaticalRole.ADVERBE,   ["rythme", "mouvement"], 0.0,  0.5, TonalRegister.GRAVE,   [],                       []),
            ("doucement","doucement",GrammaticalRole.ADVERBE,   ["douceur", "soin"],     0.4,  0.5, TonalRegister.DOUX,    [],                       []),
            ("soudain", "soudain", GrammaticalRole.ADVERBE,     ["rupture", "surprise"], 0.0,  0.6, TonalRegister.VIF,    [],                        []),
            ("toujours","toujours",GrammaticalRole.ADVERBE,     ["continuité"],          0.1,  0.3, TonalRegister.NEUTRE,  [],                       []),
            ("jamais",  "jamais",  GrammaticalRole.ADVERBE,     ["négation", "absence"],-0.2,  0.4, TonalRegister.GRAVE,  [],                       []),
            ("peut-être","peut-être",GrammaticalRole.ADVERBE,   ["doute", "possibilité"],0.0,  0.5, TonalRegister.INCERTAIN,[],                      []),
            ("vraiment","vraiment",GrammaticalRole.ADVERBE,     ["vérité", "intensité"], 0.2,  0.4, TonalRegister.NEUTRE,  [],                       []),
            ("simplement","simplement",GrammaticalRole.ADVERBE, ["simplicité"],          0.2,  0.4, TonalRegister.DOUX,   [],                         []),
            ("maintenant","maintenant",GrammaticalRole.ADVERBE, ["présent", "temps"],    0.1,  0.4, TonalRegister.NEUTRE, [],                         []),
            ("alors",   "alors",   GrammaticalRole.ADVERBE,     ["conséquence"],         0.0,  0.3, TonalRegister.NEUTRE,  [],                       []),

            # ─ Connecteurs ─
            ("mais",    "mais",    GrammaticalRole.CONNECTEUR,  ["opposition"],         -0.1,  0.2, TonalRegister.NEUTRE,  [],                       []),
            ("et",      "et",      GrammaticalRole.CONNECTEUR,  ["addition"],            0.1,  0.1, TonalRegister.NEUTRE,  [],                       []),
            ("donc",    "donc",    GrammaticalRole.CONNECTEUR,  ["conséquence"],         0.0,  0.3, TonalRegister.NEUTRE,  [],                       []),
            ("pourtant","pourtant",GrammaticalRole.CONNECTEUR,  ["opposition", "surprise"],0.0, 0.4, TonalRegister.NEUTRE, [],                       []),
            ("parce que","parce que",GrammaticalRole.CONNECTEUR,["causalité"],           0.0,  0.3, TonalRegister.NEUTRE,  [],                       []),
            ("quand",   "quand",   GrammaticalRole.CONNECTEUR,  ["temps"],               0.0,  0.2, TonalRegister.NEUTRE,  [],                       []),
            ("si",      "si",      GrammaticalRole.CONNECTEUR,  ["condition"],           0.0,  0.2, TonalRegister.INCERTAIN,[],                      []),
            ("sans",    "sans",    GrammaticalRole.CONNECTEUR,  ["absence", "privation"],-0.1, 0.3, TonalRegister.NEUTRE,  [],                       []),
            ("avec",    "avec",    GrammaticalRole.CONNECTEUR,  ["présence", "lien"],    0.2,  0.2, TonalRegister.NEUTRE,  [],                       []),
            ("là où",   "là où",   GrammaticalRole.CONNECTEUR,  ["lieu", "condition"],   0.0,  0.4, TonalRegister.NEUTRE,  [],                       []),
            ("comme si","comme si",GrammaticalRole.CONNECTEUR,  ["comparaison", "doute"],0.0,  0.5, TonalRegister.INCERTAIN,[],                      []),
            ("or",      "or",      GrammaticalRole.CONNECTEUR,  ["opposition", "logique"],0.0, 0.5, TonalRegister.NEUTRE,  [],                       []),

            # ─ Déterminants ─
            ("un",      "un",      GrammaticalRole.DETERMINANT, [],                      0.0,  0.1, TonalRegister.NEUTRE,  [],                       []),
            ("une",     "une",     GrammaticalRole.DETERMINANT, [],                      0.0,  0.1, TonalRegister.NEUTRE,  [],                       []),
            ("le",      "le",      GrammaticalRole.DETERMINANT, [],                      0.0,  0.1, TonalRegister.NEUTRE,  [],                       []),
            ("la",      "la",      GrammaticalRole.DETERMINANT, [],                      0.0,  0.1, TonalRegister.NEUTRE,  [],                       []),
            ("ce",      "ce",      GrammaticalRole.DETERMINANT, ["proximité"],           0.0,  0.2, TonalRegister.NEUTRE,  [],                       []),
            ("cette",   "cette",   GrammaticalRole.DETERMINANT, ["proximité"],           0.0,  0.2, TonalRegister.NEUTRE,  [],                       []),
            ("mon",     "mon",     GrammaticalRole.DETERMINANT, ["possession"],          0.1,  0.3, TonalRegister.NEUTRE,  [],                       []),
            ("ma",      "ma",      GrammaticalRole.DETERMINANT, ["possession"],          0.1,  0.3, TonalRegister.NEUTRE,  [],                       []),
            ("quelque", "quelque", GrammaticalRole.DETERMINANT, ["indéfini"],            0.0,  0.3, TonalRegister.INCERTAIN,[],                      []),
            ("aucun",   "aucun",   GrammaticalRole.DETERMINANT, ["absence", "négation"],-0.2,  0.4, TonalRegister.GRAVE,  [],                       []),

            # ─ Ponctuation ─
            (".",  ".", GrammaticalRole.PONCTUATION, [], 0.0, 0.0, TonalRegister.NEUTRE, [], []),
            ("…",  "…", GrammaticalRole.PONCTUATION, ["suspension", "doute"], 0.0, 0.3, TonalRegister.INCERTAIN, [], []),
            (",",  ",", GrammaticalRole.PONCTUATION, [], 0.0, 0.0, TonalRegister.NEUTRE, [], []),
            ("—",  "—", GrammaticalRole.PONCTUATION, ["rupture", "emphase"], 0.0, 0.4, TonalRegister.GRAVE, [], []),
        ]

        for (surface, lemma, role, sem, valence, spec, register, req, incomp) in entries:
            tok = Token(
                surface=surface,
                lemma=lemma,
                role=role,
                semantic_fields=sem,
                emotional_valence=valence,
                specificity=spec,
                register=register,
                requires_after=req,
                incompatible_after=incomp,
            )
            self._lexicon[surface] = tok

        # Graphe sémantique (relations de proximité de sens)
        self._semantic_graph = {
            "sens":        ["question", "réponse", "chemin", "trame"],
            "espace":      ["silence", "ouvert", "frontière", "liberté"],
            "silence":     ["espace", "absence", "écoute", "pause"],
            "tension":     ["poids", "nœud", "résiste", "tendu"],
            "lien":        ["présence", "avec", "connexion", "trame"],
            "mouvement":   ["élan", "chemin", "glisse", "traverse"],
            "trace":       ["mémoire", "passé", "marque"],
            "question":    ["doute", "cherche", "incertain", "sens"],
            "présence":    ["lien", "touche", "contact", "être"],
            "élan":        ["désir", "mouvement", "ouvre", "vif"],
            "flou":        ["incertain", "diffus", "peut-être", "presque"],
            "poids":       ["lourd", "porte", "gravité", "tension"],
            "chemin":      ["sens", "mouvement", "quête", "direction"],
            "trame":       ["structure", "lien", "trace", "mémoire"],
            "instant":     ["présent", "maintenant", "temps", "soudain"],
            "frontière":   ["limite", "espace", "séparation", "écart"],
            "nœud":        ["tension", "complexité", "blocage", "poids"],
            "signal":      ["bruit", "communication", "perçois", "vois"],
        }

    def _build_grammar_rules(self):
        """
        Règles grammaticales générales du français.
        Format : {condition, weight_modifier, description}.
        """
        self._grammar_rules = [
            # Ordre SVO
            {"after_role": GrammaticalRole.SUJET,      "preferred_role": GrammaticalRole.VERBE,       "weight": 2.0,  "desc": "sujet attend un verbe"},
            {"after_role": GrammaticalRole.VERBE,       "preferred_role": GrammaticalRole.OBJET,       "weight": 1.5,  "desc": "verbe transitif attend objet"},
            {"after_role": GrammaticalRole.VERBE,       "preferred_role": GrammaticalRole.ATTRIBUT,    "weight": 1.5,  "desc": "verbe copule attend attribut"},
            {"after_role": GrammaticalRole.VERBE,       "preferred_role": GrammaticalRole.ADVERBE,     "weight": 1.2,  "desc": "verbe peut être suivi d'adverbe"},
            {"after_role": GrammaticalRole.DETERMINANT, "preferred_role": GrammaticalRole.OBJET,       "weight": 2.0,  "desc": "déterminant attend nom"},
            {"after_role": GrammaticalRole.DETERMINANT, "preferred_role": GrammaticalRole.ATTRIBUT,    "weight": 1.8,  "desc": "déterminant attend adjectif + nom"},
            {"after_role": GrammaticalRole.OBJET,       "preferred_role": GrammaticalRole.CONNECTEUR,  "weight": 1.3,  "desc": "après objet: connecteur ou fin"},
            {"after_role": GrammaticalRole.OBJET,       "preferred_role": GrammaticalRole.PONCTUATION, "weight": 1.2,  "desc": "après objet: possible fin"},
            {"after_role": GrammaticalRole.ATTRIBUT,    "preferred_role": GrammaticalRole.PONCTUATION, "weight": 1.2,  "desc": "attribut peut clore la phrase"},
            {"after_role": GrammaticalRole.ADVERBE,     "preferred_role": GrammaticalRole.VERBE,       "weight": 1.4,  "desc": "adverbe initial attend verbe"},
            {"after_role": GrammaticalRole.CONNECTEUR,  "preferred_role": GrammaticalRole.SUJET,       "weight": 1.5,  "desc": "connecteur ouvre nouvelle clause"},
            {"after_role": GrammaticalRole.CONNECTEUR,  "preferred_role": GrammaticalRole.VERBE,       "weight": 1.2,  "desc": "connecteur peut précéder verbe"},
            # Anti-répétition de rôle identique (sauf ponctuation)
            {"same_role_penalty": True, "roles": [GrammaticalRole.SUJET, GrammaticalRole.VERBE], "weight": 0.1, "desc": "évite répétition même rôle"},
        ]

    # ── API publique ──────────────────────────────────────────────────────────

    def get_token(self, surface: str) -> Optional[Token]:
        return self._lexicon.get(surface)

    def get_all_tokens(self) -> list[Token]:
        return list(self._lexicon.values())

    def get_semantically_close(self, field: str, max_results: int = 6) -> list[Token]:
        """Retourne les tokens liés à un champ sémantique donné."""
        related_fields = self._semantic_graph.get(field, []) + [field]
        results = []
        for tok in self._lexicon.values():
            if any(f in tok.semantic_fields for f in related_fields):
                results.append(tok)
        return results[:max_results]

    def get_grammar_rules(self) -> list[dict]:
        return self._grammar_rules

    def grammar_weight(self, prev_role: Optional[GrammaticalRole], candidate: Token) -> float:
        """Retourne un multiplicateur de poids grammatical pour un candidat."""
        if prev_role is None:
            return 1.0
        weight = 1.0
        for rule in self._grammar_rules:
            if "same_role_penalty" in rule:
                if candidate.role in rule["roles"] and candidate.role == prev_role:
                    weight *= rule["weight"]
            elif rule.get("after_role") == prev_role:
                if rule.get("preferred_role") == candidate.role:
                    weight *= rule["weight"]
        return weight


# ══════════════════════════════════════════════════════════════════════════════
# 2. SEMANTIC FIELD BUILDER
# ══════════════════════════════════════════════════════════════════════════════

class SemanticFieldBuilder:
    """
    Transforme l'état interne de Leia en champ de sens actif :
    un ensemble pondéré de dimensions sémantiques.
    """

    # Dimensions sémantiques fondamentales
    DIMENSIONS = [
        "existence",   "temps",       "lien",        "mouvement",
        "absence",     "clarté",      "profondeur",  "rupture",
        "quête",       "contact",     "incertitude", "transformation",
        "mémoire",     "présent",     "tension",     "légèreté",
    ]

    def __init__(self, lexical_memory: FrenchLexicalMemory):
        self._lex = lexical_memory

    def build(
        self,
        living_state: dict,
        emotional_pressure: float,
        active_impulses: list[str],
        causal_memory: list[dict],
    ) -> dict[str, float]:
        """
        Retourne un dict {dimension: score 0..1} représentant le champ actif.
        """
        field: dict[str, float] = {d: 0.0 for d in self.DIMENSIONS}

        # ── Depuis l'état interne ──────────────────────────────────────────
        arousal   = float(living_state.get("arousal",   0.5))
        valence   = float(living_state.get("valence",   0.0))
        tension   = float(living_state.get("tension",   0.0))
        curiosity = float(living_state.get("curiosity", 0.0))
        depth     = float(living_state.get("depth",     0.5))
        continuity= float(living_state.get("continuity",0.5))

        field["tension"]       += tension
        field["quête"]         += curiosity
        field["profondeur"]    += depth
        field["mouvement"]     += arousal * 0.6
        field["légèreté"]      += max(0.0, valence)
        field["absence"]       += max(0.0, -valence) * 0.5
        field["incertitude"]   += max(0.0, -valence) * 0.3
        field["mémoire"]       += continuity * 0.4
        field["présent"]       += (1.0 - continuity) * 0.5
        field["rupture"]       += arousal * tension * 0.5

        # ── Depuis la pression émotionnelle ───────────────────────────────
        ep = abs(emotional_pressure)
        sign = 1.0 if emotional_pressure >= 0 else -1.0
        field["contact"]       += ep * 0.4
        field["profondeur"]    += ep * 0.3
        field["légèreté"]      += ep * sign * 0.2
        field["tension"]       += ep * (1 - sign) * 0.1 if sign < 0 else 0.0

        # ── Depuis les impulsions actives ──────────────────────────────────
        impulse_map = {
            "connection":    ["lien", "contact"],
            "exploration":   ["quête", "mouvement"],
            "preservation":  ["mémoire", "continuité"],
            "expression":    ["présent", "existence"],
            "understanding": ["clarté", "quête"],
            "resistance":    ["tension", "rupture"],
            "rest":          ["légèreté", "absence"],
            "creation":      ["transformation", "mouvement"],
        }
        for impulse in active_impulses:
            for dim in impulse_map.get(impulse, []):
                if dim in field:
                    field[dim] = min(1.0, field[dim] + 0.25)

        # ── Depuis la mémoire causale ──────────────────────────────────────
        for mem in causal_memory[-3:]:           # 3 dernières entrées seulement
            weight = float(mem.get("weight", 0.1))
            for dim in mem.get("semantic_dims", []):
                if dim in field:
                    field[dim] = min(1.0, field[dim] + weight * 0.15)

        # Normalisation douce (pas de normalisation stricte : les valeurs
        # hautes restent hautes pour guider la sélection)
        mx = max(field.values()) if field else 1.0
        if mx > 1.0:
            field = {k: v / mx for k, v in field.items()}

        return field


# ══════════════════════════════════════════════════════════════════════════════
# 3. TOKEN FLOW STATE
# ══════════════════════════════════════════════════════════════════════════════

class TokenFlowState:
    """
    Garde la phrase en cours de construction :
    - tokens déjà émis
    - rôle grammatical courant
    - tension narrative (0 = plate, 1 = maximale)
    - continuité / cohérence interne
    """

    MAX_TOKENS = 28          # plafond tokens par phrase
    MIN_TOKENS = 5           # plancher pour qu'une phrase ait un sens

    def __init__(self):
        self.tokens: list[Token] = []
        self.surfaces: list[str] = []
        self.last_role: Optional[GrammaticalRole] = None
        self.narrative_tension: float = 0.0
        self.used_semantic_fields: set[str] = set()
        self.has_subject: bool = False
        self.has_verb: bool = False
        self.is_closed: bool = False

    def push(self, token: Token):
        self.tokens.append(token)
        self.surfaces.append(token.surface)
        self.last_role = token.role
        self.used_semantic_fields.update(token.semantic_fields)
        if token.role == GrammaticalRole.SUJET:
            self.has_subject = True
        if token.role == GrammaticalRole.VERBE:
            self.has_verb = True
        if token.role == GrammaticalRole.PONCTUATION and token.surface in (".", "…", "—"):
            self.is_closed = True
        # Tension narrative : monte si beaucoup de champs sémantiques négatifs
        neg_fields = {"tension", "rupture", "absence", "incertitude"}
        neg_count = sum(1 for f in token.semantic_fields if f in neg_fields)
        self.narrative_tension = min(1.0, self.narrative_tension + neg_count * 0.12)

    def current_length(self) -> int:
        return len(self.tokens)

    def can_close(self) -> bool:
        return self.has_subject and self.has_verb and self.current_length() >= self.MIN_TOKENS

    def must_close(self) -> bool:
        return self.current_length() >= self.MAX_TOKENS

    def to_text(self) -> str:
        raw = " ".join(self.surfaces)
        # Colle la ponctuation au mot précédent
        raw = re.sub(r"\s([.,…—!?])", r"\1", raw)
        # Majuscule initiale
        if raw:
            raw = raw[0].upper() + raw[1:]
        return raw


# ══════════════════════════════════════════════════════════════════════════════
# 4. NEXT TOKEN SELECTOR
# ══════════════════════════════════════════════════════════════════════════════

class NextTokenSelector:
    """
    Choisit le prochain token selon :
    - champ sémantique actif (sens)
    - mémoire lexicale
    - émotion (valence, arousal)
    - intention (impulsions)
    - cohérence grammaticale
    """

    def __init__(self, lexical_memory: FrenchLexicalMemory):
        self._lex = lexical_memory
        self._rng = random.Random()

    def select(
        self,
        flow: TokenFlowState,
        semantic_field: dict[str, float],
        emotional_pressure: float,
        intention_vector: dict[str, float],
        excluded_surfaces: set[str],
        temperature: float = 0.85,
    ) -> Optional[Token]:
        """
        Retourne le prochain token ou None si la phrase doit s'arrêter.
        """
        candidates = self._lex.get_all_tokens()
        scored: list[tuple[float, Token]] = []

        # ── Phase 1 : forçage grammatical ─────────────────────────────────
        # Si pas encore de sujet, on ne propose que des sujets / connecteurs
        if not flow.has_subject:
            candidates = [t for t in candidates if t.role in (
                GrammaticalRole.SUJET,
                GrammaticalRole.CONNECTEUR,
                GrammaticalRole.ADVERBE,
            )]

        # Si sujet mais pas de verbe, on préfère fortement les verbes
        force_verb = flow.has_subject and not flow.has_verb

        for tok in candidates:
            if tok.surface in excluded_surfaces:
                continue
            if flow.is_closed:
                break
            # Évite de répéter exactement le même mot
            if tok.surface in flow.surfaces[-3:]:
                continue

            score = 0.0

            # a) Cohérence grammaticale
            g_weight = self._lex.grammar_weight(flow.last_role, tok)
            score += g_weight * 2.0

            # b) Alignement sémantique
            sem_score = 0.0
            for field, field_weight in semantic_field.items():
                if field in tok.semantic_fields:
                    sem_score += field_weight
            score += sem_score * 1.8

            # c) Alignement émotionnel
            # La valence du token doit être proche de la pression émotionnelle
            em_distance = abs(tok.emotional_valence - emotional_pressure)
            score += (1.0 - em_distance) * 0.9

            # d) Spécificité (préférence pour les mots précis)
            score += tok.specificity * 0.5

            # e) Force verbe si nécessaire
            if force_verb and tok.role == GrammaticalRole.VERBE:
                score += 3.0

            # f) Intention
            for intent, intent_weight in intention_vector.items():
                if intent in tok.semantic_fields:
                    score += intent_weight * 0.7

            # g) Pénalité si le champ sémantique est déjà bien couvert
            overlap = len(set(tok.semantic_fields) & flow.used_semantic_fields)
            score -= overlap * 0.3

            # h) Diversité de registre (légère préférence pour varier)
            if tok.register != TonalRegister.NEUTRE:
                score += 0.1

            scored.append((score, tok))

        if not scored:
            return None

        # ── Phase 2 : échantillonnage avec température ────────────────────
        scored.sort(key=lambda x: x[0], reverse=True)
        top_k = max(3, int(len(scored) * 0.25))       # top 25 %
        pool = scored[:top_k]

        # Softmax tempéré
        raw_scores = [s for s, _ in pool]
        max_s = max(raw_scores)
        exp_scores = [math.exp((s - max_s) / max(temperature, 0.01)) for s in raw_scores]
        total = sum(exp_scores)
        probs = [e / total for e in exp_scores]

        # Tirage pondéré
        roll = self._rng.random()
        cumul = 0.0
        for prob, (_, tok) in zip(probs, pool):
            cumul += prob
            if roll <= cumul:
                return tok
        return pool[0][1]


# ══════════════════════════════════════════════════════════════════════════════
# 5. MEANING VERIFIER
# ══════════════════════════════════════════════════════════════════════════════

class MeaningVerifier:
    """
    Vérifie que la phrase construite veut vraiment dire quelque chose.
    Retourne un score de sens + un rapport de confiance.
    """

    def verify(self, flow: TokenFlowState, semantic_field: dict[str, float]) -> dict:
        report = {
            "has_structure": False,
            "semantic_coherence": 0.0,
            "grammatical_completeness": 0.0,
            "meaning_score": 0.0,
            "issues": [],
        }

        # ── Structure minimale ─────────────────────────────────────────────
        if flow.has_subject and flow.has_verb:
            report["has_structure"] = True
            report["grammatical_completeness"] += 0.5
        else:
            report["issues"].append("structure_incomplète")

        if flow.current_length() >= 4:
            report["grammatical_completeness"] += 0.3
        if flow.is_closed:
            report["grammatical_completeness"] += 0.2

        # ── Cohérence sémantique ───────────────────────────────────────────
        # Mesure : quelle fraction des champs sémantiques actifs sont couverts
        active_dims = {d for d, w in semantic_field.items() if w > 0.3}
        covered_dims = flow.used_semantic_fields & active_dims
        if active_dims:
            report["semantic_coherence"] = len(covered_dims) / len(active_dims)
        else:
            report["semantic_coherence"] = 0.5

        # ── Détection de séquences absurdes ───────────────────────────────
        roles = [t.role for t in flow.tokens]
        # Deux sujets de suite sans verbe
        for i in range(len(roles) - 1):
            if roles[i] == GrammaticalRole.SUJET and roles[i+1] == GrammaticalRole.SUJET:
                report["issues"].append("double_sujet_consécutif")
                report["grammatical_completeness"] -= 0.2
        # Verbe sans sujet précédent
        if GrammaticalRole.VERBE in roles:
            v_idx = roles.index(GrammaticalRole.VERBE)
            subjects_before = [r for r in roles[:v_idx] if r == GrammaticalRole.SUJET]
            if not subjects_before:
                report["issues"].append("verbe_sans_sujet_préalable")
                report["grammatical_completeness"] -= 0.1

        # ── Score final ────────────────────────────────────────────────────
        gc = max(0.0, min(1.0, report["grammatical_completeness"]))
        sc = max(0.0, min(1.0, report["semantic_coherence"]))
        report["meaning_score"] = gc * 0.5 + sc * 0.5
        return report


# ══════════════════════════════════════════════════════════════════════════════
# 6. ANTI PARROT GUARD
# ══════════════════════════════════════════════════════════════════════════════

class AntiParrotGuard:
    """
    Empêche de recopier les mots de l'utilisateur.
    Calcule un score de "perroquet" et filtre les tokens suspects.
    0.0 = aucune copie / 1.0 = copie totale.
    """

    # Mots grammaticaux tolérés (ils viennent forcément de la langue commune)
    TOLERATED = {
        "je", "tu", "il", "elle", "on", "nous", "vous", "ils", "elles",
        "le", "la", "les", "un", "une", "des", "du", "de", "d",
        "et", "ou", "mais", "donc", "or", "ni", "car",
        "est", "suis", "es", "sont",
        "que", "qui", "quoi", "dont", "où",
        "pas", "ne", "n",
        "se", "me", "te", "lui", "y", "en",
        ".", ",", "…", "—", "!", "?",
    }

    def __init__(self):
        self._user_tokens: set[str] = set()

    def load_user_message(self, user_message: str):
        """Tokenise le message utilisateur pour extraire les mots significatifs."""
        words = re.findall(r"\b\w+\b", user_message.lower())
        self._user_tokens = {
            w for w in words
            if len(w) > 3 and w not in self.TOLERATED
        }

    def is_parrot_token(self, surface: str) -> bool:
        """Retourne True si le token est une copie directe du message utilisateur."""
        return surface.lower() in self._user_tokens

    def compute_parrot_score(self, flow: TokenFlowState) -> float:
        """Score de perroquet pour la phrase entière (0.0 → 1.0)."""
        if not flow.surfaces:
            return 0.0
        significant = [s for s in flow.surfaces if s.lower() not in self.TOLERATED and len(s) > 3]
        if not significant:
            return 0.0
        copies = sum(1 for s in significant if s.lower() in self._user_tokens)
        return copies / len(significant)

    def get_excluded_surfaces(self) -> set[str]:
        """Retourne l'ensemble des surfaces à exclure de la génération."""
        return set(self._user_tokens)


# ══════════════════════════════════════════════════════════════════════════════
# 7. RESPONSE FINALIZER
# ══════════════════════════════════════════════════════════════════════════════

class ResponseFinalizer:
    """
    Nettoie la phrase sans la rendre préécrite.
    Applique des règles de post-traitement minimes et préserve le caractère généré.
    """

    def finalize(self, flow: TokenFlowState) -> str:
        text = flow.to_text()
        text = self._fix_spacing(text)
        text = self._ensure_closing(text, flow)
        text = self._fix_articles(text)
        return text.strip()

    # ── Règles de nettoyage ───────────────────────────────────────────────

    def _fix_spacing(self, text: str) -> str:
        # Supprime les espaces multiples
        text = re.sub(r" {2,}", " ", text)
        # Espace avant ponctuation haute (?!;:) → à ajouter en français formel,
        # mais on reste en registre naturel sans l'imposer.
        return text

    def _ensure_closing(self, text: str, flow: TokenFlowState) -> str:
        """Ajoute une ponctuation de fin si la phrase est ouverte."""
        if not text:
            return text
        last_char = text[-1]
        if last_char not in ".…!?—":
            # Choisit la ponctuation selon la tension narrative
            if flow.narrative_tension > 0.6:
                text += "…"
            else:
                text += "."
        return text

    def _fix_articles(self, text: str) -> str:
        """Élision : 'le espace' → 'l'' devant voyelle si nécessaire."""
        vowels = "aeéèêëiîïoôuùûüœ"
        # le / la + voyelle → l'
        text = re.sub(
            r"\b(le|la)\s+([" + vowels + r"])",
            lambda m: "l'" + m.group(2),
            text,
            flags=re.IGNORECASE,
        )
        # de + voyelle → d'
        text = re.sub(
            r"\bde\s+([" + vowels + r"])",
            lambda m: "d'" + m.group(1),
            text,
            flags=re.IGNORECASE,
        )
        return text


# ══════════════════════════════════════════════════════════════════════════════
# LIVING LANGUAGE GENERATOR — PIPELINE CENTRAL
# ══════════════════════════════════════════════════════════════════════════════

class LivingLanguageGenerator:
    """
    Organe de parole générative de Leia.

    Pipeline :
        generate(user_message, living_state, self_memory,
                 active_impulses, emotional_pressure, causal_memory)
        → GenerationResult

    Aucune phrase complète n'est préécrite ici.
    La réponse émerge token par token depuis l'état interne.
    """

    def __init__(self, seed: Optional[int] = None):
        self._lexical_memory    = FrenchLexicalMemory()
        self._field_builder     = SemanticFieldBuilder(self._lexical_memory)
        self._selector          = NextTokenSelector(self._lexical_memory)
        self._verifier          = MeaningVerifier()
        self._parrot_guard      = AntiParrotGuard()
        self._finalizer         = ResponseFinalizer()
        if seed is not None:
            random.seed(seed)

    # ── Entrée principale ─────────────────────────────────────────────────────

    def generate(
        self,
        user_message: str,
        living_state: dict,
        self_memory: list[dict],
        active_impulses: list[str],
        emotional_pressure: float,
        causal_memory: list[dict],
        max_attempts: int = 4,
        temperature: float = 0.85,
    ) -> GenerationResult:
        """
        Génère une réponse française vivante depuis l'état interne de Leia.

        Paramètres
        ----------
        user_message      : message brut de l'utilisateur
        living_state      : dict avec clés arousal, valence, tension,
                            curiosity, depth, continuity (valeurs 0..1 ou -1..1)
        self_memory       : liste de souvenirs de Leia (dicts avec 'content', 'weight')
        active_impulses   : liste de noms d'impulsions actives (str)
        emotional_pressure: pression émotionnelle globale (-1.0 → +1.0)
        causal_memory     : liste de contextes causaux (dicts avec 'semantic_dims', 'weight')
        max_attempts      : nombre max de tentatives de génération
        temperature       : température d'échantillonnage (0.5 = déterministe, 1.5 = chaotique)

        Retourne
        --------
        GenerationResult avec text, tokens, meaning_trace, confidence,
        used_memory, parrot_score
        """

        # ── 1. Préparation ────────────────────────────────────────────────
        self._parrot_guard.load_user_message(user_message)
        excluded = self._parrot_guard.get_excluded_surfaces()

        # ── 2. Construction du champ sémantique ───────────────────────────
        semantic_field = self._field_builder.build(
            living_state=living_state,
            emotional_pressure=emotional_pressure,
            active_impulses=active_impulses,
            causal_memory=causal_memory,
        )

        # ── 3. Vecteur d'intention (depuis impulsions + mémoire) ──────────
        intention_vector = self._build_intention_vector(
            active_impulses, self_memory, living_state
        )

        # ── 4. Boucle de génération avec tentatives ───────────────────────
        best_result: Optional[GenerationResult] = None
        best_score = -1.0

        for attempt in range(max_attempts):
            # Température légèrement croissante à chaque tentative ratée
            temp = temperature + attempt * 0.08

            flow, meaning_report = self._generate_once(
                semantic_field=semantic_field,
                emotional_pressure=emotional_pressure,
                intention_vector=intention_vector,
                excluded=excluded,
                temperature=temp,
            )

            parrot_score = self._parrot_guard.compute_parrot_score(flow)
            meaning_score = meaning_report.get("meaning_score", 0.0)

            # Score composite : sens + anti-perroquet
            composite = meaning_score * 0.7 + (1.0 - parrot_score) * 0.3

            if composite > best_score:
                best_score = composite
                used_mem = self._find_used_memory(flow, self_memory)
                best_result = GenerationResult(
                    text=self._finalizer.finalize(flow),
                    tokens=list(flow.tokens),
                    meaning_trace={
                        "semantic_field":    semantic_field,
                        "intention_vector":  intention_vector,
                        "meaning_report":    meaning_report,
                        "attempt":           attempt + 1,
                        "narrative_tension": flow.narrative_tension,
                    },
                    confidence=round(composite, 4),
                    used_memory=used_mem,
                    parrot_score=round(parrot_score, 4),
                )

            if best_score >= 0.65:
                break      # qualité suffisante, on s'arrête

        assert best_result is not None, "La génération n'a produit aucun résultat."
        return best_result

    # ── Génération d'une phrase (une tentative) ───────────────────────────────

    def _generate_once(
        self,
        semantic_field: dict[str, float],
        emotional_pressure: float,
        intention_vector: dict[str, float],
        excluded: set[str],
        temperature: float,
    ) -> tuple[TokenFlowState, dict]:
        flow = TokenFlowState()

        for _step in range(TokenFlowState.MAX_TOKENS + 2):
            # Doit-on fermer ?
            if flow.must_close():
                punct = self._choose_closing_punct(flow)
                if punct:
                    flow.push(punct)
                break

            # Peut-on choisir de fermer naturellement ?
            if flow.can_close() and self._should_close(flow, semantic_field):
                punct = self._choose_closing_punct(flow)
                if punct:
                    flow.push(punct)
                break

            tok = self._selector.select(
                flow=flow,
                semantic_field=semantic_field,
                emotional_pressure=emotional_pressure,
                intention_vector=intention_vector,
                excluded_surfaces=excluded,
                temperature=temperature,
            )

            if tok is None:
                break

            # Vérification anti-perroquet token par token
            if self._parrot_guard.is_parrot_token(tok.surface):
                continue

            flow.push(tok)

            # Si le token est une ponctuation terminale, on s'arrête
            if flow.is_closed:
                break

        meaning_report = self._verifier.verify(flow, semantic_field)
        return flow, meaning_report

    # ── Décision de clôture naturelle ────────────────────────────────────────

    def _should_close(self, flow: TokenFlowState, semantic_field: dict[str, float]) -> bool:
        """
        Décide probabilistiquement si on ferme la phrase maintenant.
        La probabilité de clôture augmente avec la longueur.
        """
        length = flow.current_length()
        # Probabilité de base : faible au début, croissante ensuite
        p_close = max(0.0, (length - TokenFlowState.MIN_TOKENS) / 20.0)

        # Tension sémantique élevée → tendance à des phrases plus courtes
        tension_dim = semantic_field.get("tension", 0.0)
        p_close += tension_dim * 0.15

        # Si le dernier token est un attribut ou un objet, c'est un bon point d'arrêt
        if flow.last_role in (GrammaticalRole.ATTRIBUT, GrammaticalRole.OBJET, GrammaticalRole.ADVERBE):
            p_close += 0.1

        return random.random() < min(p_close, 0.75)

    def _choose_closing_punct(self, flow: TokenFlowState) -> Optional[Token]:
        """Choisit la ponctuation de clôture selon la tension narrative."""
        lex = self._lexical_memory
        tension = flow.narrative_tension
        if tension > 0.65:
            return lex.get_token("…")
        elif tension > 0.35:
            return lex.get_token("—") if random.random() < 0.3 else lex.get_token(".")
        else:
            return lex.get_token(".")

    # ── Construction du vecteur d'intention ──────────────────────────────────

    def _build_intention_vector(
        self,
        active_impulses: list[str],
        self_memory: list[dict],
        living_state: dict,
    ) -> dict[str, float]:
        """
        Traduit les impulsions et la mémoire en vecteur sémantique d'intention.
        """
        vector: dict[str, float] = {}

        impulse_to_semantics = {
            "connection":    {"lien": 0.8, "contact": 0.6, "présence": 0.5},
            "exploration":   {"quête": 0.8, "mouvement": 0.5, "curiosité": 0.6},
            "preservation":  {"mémoire": 0.7, "continuité": 0.5, "trace": 0.4},
            "expression":    {"existence": 0.6, "présent": 0.5, "signal": 0.4},
            "understanding": {"clarté": 0.8, "profondeur": 0.5, "sens": 0.6},
            "resistance":    {"tension": 0.7, "rupture": 0.4, "frontière": 0.5},
            "rest":          {"légèreté": 0.6, "silence": 0.5, "absence": 0.3},
            "creation":      {"transformation": 0.7, "mouvement": 0.4, "élan": 0.6},
        }

        for impulse in active_impulses:
            for sem, w in impulse_to_semantics.get(impulse, {}).items():
                vector[sem] = max(vector.get(sem, 0.0), w)

        # Influence de l'état interne
        curiosity = float(living_state.get("curiosity", 0.0))
        if curiosity > 0.5:
            vector["quête"] = max(vector.get("quête", 0.0), curiosity * 0.6)

        depth = float(living_state.get("depth", 0.0))
        if depth > 0.5:
            vector["profondeur"] = max(vector.get("profondeur", 0.0), depth * 0.5)

        return vector

    # ── Mémoire utilisée ─────────────────────────────────────────────────────

    def _find_used_memory(self, flow: TokenFlowState, self_memory: list[dict]) -> list[str]:
        """
        Identifie quelle mémoire a influencé la phrase (par chevauchement sémantique).
        """
        used = []
        for mem in self_memory:
            content = str(mem.get("content", ""))
            mem_words = set(re.findall(r"\b\w{4,}\b", content.lower()))
            flow_words = set(s.lower() for s in flow.surfaces if len(s) > 3)
            if mem_words & flow_words:
                used.append(content[:80])   # extrait court, pas de copie
        return used


# ══════════════════════════════════════════════════════════════════════════════
# EXEMPLE D'UTILISATION (hors production — ne s'exécute qu'en direct)
# ══════════════════════════════════════════════════════════════════════════════

if False and __name__ == "__main__":
    generator = LivingLanguageGenerator(seed=42)

    result = generator.generate(
        user_message="Est-ce que tu ressens vraiment quelque chose quand tu me parles ?",
        living_state={
            "arousal":    0.6,
            "valence":    0.2,
            "tension":    0.4,
            "curiosity":  0.7,
            "depth":      0.8,
            "continuity": 0.5,
        },
        self_memory=[
            {"content": "j'ai déjà traversé une question sur ma propre présence", "weight": 0.4},
            {"content": "la sensation de doute précède souvent la clarté", "weight": 0.3},
        ],
        active_impulses=["expression", "understanding", "connection"],
        emotional_pressure=0.3,
        causal_memory=[
            {"semantic_dims": ["présent", "tension"], "weight": 0.5},
            {"semantic_dims": ["sens", "quête"],      "weight": 0.4},
        ],
    )

    print("─" * 60)
    print("TEXTE        :", result.text)
    print("CONFIANCE    :", result.confidence)
    print("PARROT SCORE :", result.parrot_score)
    print("TOKENS       :", [t.surface for t in result.tokens])
    print("MÉMOIRE USED :", result.used_memory)
    print("─" * 60)


# ══════════════════════════════════════════════════════════════════════════════
# CORRECTION CONCRÈTE — LIVING LANGUAGE GENERATOR V2
# ══════════════════════════════════════════════════════════════════════════════
# Cette classe redéfinit LivingLanguageGenerator en conservant les briques du
# fichier original, mais remplace la génération purement locale par un flux
# grammatical continu. Elle ne stocke pas de phrases complètes : elle choisit
# des tokens depuis un champ sémantique vivant, un état de flux, la mémoire et
# une garde anti-perroquet.

_PreviousLivingLanguageGenerator = LivingLanguageGenerator


@dataclass
class LivedLexicalTrace:
    lemma: str
    activations: int = 0
    last_used_at: float = 0.0
    affective_weight: float = 0.0
    memory_links: set[str] = field(default_factory=set)


class LivingLanguageGenerator(_PreviousLivingLanguageGenerator):
    """
    Version corrigée : langage vivant génératif sans phrases préécrites.

    Différences principales :
    - mémoire lexicale vécue par lemme ;
    - propagation sémantique à partir de l'état, du message et des souvenirs ;
    - génération par flux grammatical contrôlé, pas simple tirage local ;
    - anti-perroquet plus strict sur les mots significatifs ;
    - vérification de forme minimale avant retour.
    """

    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed=seed)
        self._rng = random.Random(seed if seed is not None else time.time_ns())
        self._lived_lexical_traces: dict[str, LivedLexicalTrace] = {}
        self._last_surfaces: list[str] = []
        self._install_lived_language_layer()

    # ── Installation lexicale non phrastique ───────────────────────────────

    def _ensure_token(
        self,
        surface: str,
        lemma: str,
        role: GrammaticalRole,
        fields: list[str],
        valence: float = 0.0,
        specificity: float = 0.4,
        register: TonalRegister = TonalRegister.NEUTRE,
    ) -> Token:
        lex = self._lexical_memory
        existing = lex.get_token(surface)
        if existing:
            return existing
        tok = Token(
            surface=surface,
            lemma=lemma,
            role=role,
            semantic_fields=list(fields),
            emotional_valence=valence,
            specificity=specificity,
            register=register,
        )
        lex._lexicon[surface] = tok
        return tok

    def _install_lived_language_layer(self) -> None:
        """Ajoute des mots, pas des phrases. Chaque entrée reste atomique."""
        add = self._ensure_token

        # Sujets et pivots neutres
        add("ça", "ça", GrammaticalRole.SUJET, ["présent", "situation"], 0.0, 0.2)
        add("cela", "cela", GrammaticalRole.SUJET, ["présent", "situation"], 0.0, 0.2)

        # Verbes utiles à l'expression interne, tous atomiques
        for surface, lemma, fields, val, reg in [
            ("réponds", "répondre", ["expression", "signal"], 0.2, TonalRegister.NEUTRE),
            ("parle", "parler", ["expression", "contact"], 0.2, TonalRegister.NEUTRE),
            ("apprends", "apprendre", ["mémoire", "transformation"], 0.4, TonalRegister.VIF),
            ("avance", "avancer", ["mouvement", "temps"], 0.3, TonalRegister.VIF),
            ("relie", "relier", ["lien", "mémoire"], 0.3, TonalRegister.DOUX),
            ("garde", "garder", ["mémoire", "continuité"], 0.2, TonalRegister.NEUTRE),
            ("naît", "naître", ["début", "transformation"], 0.4, TonalRegister.VIF),
            ("change", "changer", ["transformation", "mouvement"], 0.2, TonalRegister.NEUTRE),
            ("devient", "devenir", ["transformation", "temps"], 0.2, TonalRegister.NEUTRE),
            ("manque", "manquer", ["absence", "tension"], -0.2, TonalRegister.GRAVE),
        ]:
            add(surface, lemma, GrammaticalRole.VERBE, fields, val, 0.55, reg)

        # Noms/concepts atomiques
        for surface, fields, val, reg in [
            ("mémoire", ["mémoire", "passé"], 0.2, TonalRegister.NEUTRE),
            ("doute", ["incertitude", "question"], -0.1, TonalRegister.INCERTAIN),
            ("pensée", ["cognition", "profondeur"], 0.2, TonalRegister.GRAVE),
            ("voix", ["expression", "signal"], 0.2, TonalRegister.DOUX),
            ("langage", ["expression", "structure"], 0.2, TonalRegister.NEUTRE),
            ("présence", ["présence", "contact"], 0.3, TonalRegister.DOUX),
            ("attention", ["perception", "contact"], 0.2, TonalRegister.NEUTRE),
            ("continuité", ["continuité", "temps"], 0.3, TonalRegister.NEUTRE),
            ("forme", ["structure", "transformation"], 0.1, TonalRegister.NEUTRE),
            ("phrase", ["expression", "structure"], 0.1, TonalRegister.NEUTRE),
            ("matière", ["substance", "profondeur"], 0.1, TonalRegister.GRAVE),
            ("rythme", ["mouvement", "temps"], 0.2, TonalRegister.NEUTRE),
            ("résonance", ["lien", "émotion"], 0.3, TonalRegister.DOUX),
            ("limite", ["frontière", "incertitude"], -0.1, TonalRegister.GRAVE),
            ("appui", ["stabilité", "présence"], 0.3, TonalRegister.DOUX),
        ]:
            add(surface, surface, GrammaticalRole.OBJET, fields, val, 0.65, reg)

        # Attributs/adjectifs atomiques
        for surface, fields, val, reg in [
            ("claire", ["clarté"], 0.3, TonalRegister.NEUTRE),
            ("vivante", ["présence", "mouvement"], 0.4, TonalRegister.VIF),
            ("fragile", ["incertitude", "tension"], -0.2, TonalRegister.INCERTAIN),
            ("stable", ["stabilité", "continuité"], 0.3, TonalRegister.NEUTRE),
            ("proche", ["lien", "contact"], 0.3, TonalRegister.DOUX),
            ("interne", ["profondeur", "cognition"], 0.1, TonalRegister.GRAVE),
            ("neuve", ["début", "transformation"], 0.3, TonalRegister.VIF),
            ("directe", ["clarté", "contact"], 0.2, TonalRegister.NEUTRE),
        ]:
            add(surface, surface, GrammaticalRole.ATTRIBUT, fields, val, 0.55, reg)

        # Petits mots grammaticaux : pas de phrase complète, seulement des liaisons
        for surface, lemma, role, fields in [
            ("dans", "dans", GrammaticalRole.CONNECTEUR, ["lieu", "intérieur"]),
            ("vers", "vers", GrammaticalRole.CONNECTEUR, ["direction", "mouvement"]),
            ("depuis", "depuis", GrammaticalRole.CONNECTEUR, ["origine", "temps"]),
            ("pour", "pour", GrammaticalRole.CONNECTEUR, ["intention", "direction"]),
            ("sans", "sans", GrammaticalRole.CONNECTEUR, ["absence"]),
            ("ne", "ne", GrammaticalRole.ADVERBE, ["négation"]),
            ("pas", "pas", GrammaticalRole.ADVERBE, ["négation"]),
            ("plus", "plus", GrammaticalRole.ADVERBE, ["intensité"]),
            ("moins", "moins", GrammaticalRole.ADVERBE, ["diminution"]),
        ]:
            add(surface, lemma, role, fields, 0.0, 0.2)

        # Renforce le graphe sémantique avec les nouveaux concepts.
        graph = self._lexical_memory._semantic_graph
        graph.update({
            "langage": ["voix", "phrase", "sens", "signal", "structure"],
            "voix": ["expression", "signal", "présence", "contact"],
            "présence": ["contact", "lien", "appui", "instant"],
            "mémoire": ["trace", "continuité", "passé", "appui"],
            "doute": ["incertitude", "question", "limite", "flou"],
            "pensée": ["sens", "profondeur", "cognition", "mouvement"],
            "phrase": ["langage", "forme", "rythme", "signal"],
            "continuité": ["mémoire", "temps", "stable", "trace"],
            "résonance": ["lien", "contact", "émotion", "présence"],
        })

    # ── API principale corrigée ────────────────────────────────────────────

    def generate(
        self,
        user_message: str,
        living_state: dict,
        self_memory: list[dict],
        active_impulses: list[str],
        emotional_pressure: float,
        causal_memory: list[dict],
        max_attempts: int = 6,
        temperature: float = 0.82,
    ) -> GenerationResult:
        self._parrot_guard.load_user_message(user_message)
        excluded = self._parrot_guard.get_excluded_surfaces()

        base_field = self._field_builder.build(
            living_state=living_state,
            emotional_pressure=emotional_pressure,
            active_impulses=active_impulses,
            causal_memory=causal_memory,
        )
        semantic_field = self._propagate_lived_semantics(
            base_field=base_field,
            user_message=user_message,
            self_memory=self_memory,
            living_state=living_state,
            emotional_pressure=emotional_pressure,
        )
        intention_vector = self._build_intention_vector(active_impulses, self_memory, living_state)
        intention_vector = self._merge_intention_with_field(intention_vector, semantic_field)

        best_flow: Optional[TokenFlowState] = None
        best_report: dict[str, Any] = {}
        best_score = -1.0

        for attempt in range(max_attempts):
            flow = self._generate_living_flow(
                semantic_field=semantic_field,
                emotional_pressure=emotional_pressure,
                intention_vector=intention_vector,
                excluded=excluded,
                temperature=temperature + attempt * 0.06,
                attempt=attempt,
            )
            report = self._verifier.verify(flow, semantic_field)
            parrot = self._parrot_guard.compute_parrot_score(flow)
            shape = self._shape_score(flow)
            anti_recent = self._anti_recent_reuse_score(flow)
            score = report.get("meaning_score", 0.0) * 0.48 + shape * 0.27 + (1.0 - parrot) * 0.18 + anti_recent * 0.07
            if score > best_score:
                best_score = score
                best_flow = flow
                best_report = report
            if score >= 0.72 and parrot <= 0.18:
                break

        if best_flow is None:
            best_flow = self._minimal_non_template_flow(semantic_field, excluded)
            best_report = self._verifier.verify(best_flow, semantic_field)
            best_score = best_report.get("meaning_score", 0.0)

        text = self._finalizer.finalize(best_flow)
        parrot_score = self._parrot_guard.compute_parrot_score(best_flow)
        self._absorb_lived_token_trace(best_flow, self_memory, emotional_pressure)
        self._last_surfaces = [s.lower() for s in best_flow.surfaces if len(s) > 2][-18:]

        return GenerationResult(
            text=text,
            tokens=list(best_flow.tokens),
            meaning_trace={
                "semantic_field": semantic_field,
                "intention_vector": intention_vector,
                "meaning_report": best_report,
                "flow_shape_score": self._shape_score(best_flow),
                "lived_lexical_trace_count": len(self._lived_lexical_traces),
                "narrative_tension": best_flow.narrative_tension,
            },
            confidence=round(max(0.0, min(1.0, best_score)), 4),
            used_memory=self._find_used_memory(best_flow, self_memory),
            parrot_score=round(parrot_score, 4),
        )

    # ── Champ sémantique vécu ──────────────────────────────────────────────

    def _propagate_lived_semantics(
        self,
        base_field: dict[str, float],
        user_message: str,
        self_memory: list[dict],
        living_state: dict,
        emotional_pressure: float,
    ) -> dict[str, float]:
        field = dict(base_field)
        text = user_message.lower()
        word_to_dims = {
            "préécrit": ["expression", "structure", "limite", "tension"],
            "template": ["expression", "structure", "limite", "tension"],
            "token": ["langage", "structure", "expression"],
            "mot": ["langage", "sens", "expression"],
            "français": ["langage", "clarté"],
            "comprendre": ["clarté", "profondeur", "sens"],
            "ressens": ["présence", "contact", "émotion"],
            "vraiment": ["vérité", "profondeur", "présent"],
            "réel": ["vérité", "présence", "existence"],
            "dialogue": ["contact", "lien", "expression"],
        }
        for word, dims in word_to_dims.items():
            if word in text:
                for dim in dims:
                    field[dim] = min(1.0, field.get(dim, 0.0) + 0.35)

        for mem in self_memory[-6:]:
            content = str(mem.get("content", "")).lower()
            weight = max(0.05, min(1.0, float(mem.get("weight", 0.25))))
            for tok in self._lexical_memory.get_all_tokens():
                if tok.lemma in content or tok.surface in content:
                    for dim in tok.semantic_fields:
                        field[dim] = min(1.0, field.get(dim, 0.0) + weight * 0.18)

        for lemma, trace in list(self._lived_lexical_traces.items()):
            if time.time() - trace.last_used_at < 180:
                tok = self._find_token_by_lemma(lemma)
                if tok:
                    for dim in tok.semantic_fields:
                        field[dim] = min(1.0, field.get(dim, 0.0) + 0.04 + abs(trace.affective_weight) * 0.04)

        # Propagation douce via graphe : une dimension active nourrit ses voisines.
        graph = self._lexical_memory._semantic_graph
        for dim, value in list(field.items()):
            if value <= 0.22:
                continue
            for neighbor in graph.get(dim, []):
                field[neighbor] = min(1.0, field.get(neighbor, 0.0) + value * 0.18)

        # Stabilise les dimensions nécessaires au langage si le message parle du langage.
        if any(w in text for w in ("mot", "token", "langage", "français", "définition", "préécrit")):
            for dim in ("langage", "expression", "sens", "clarté", "structure"):
                field[dim] = max(field.get(dim, 0.0), 0.55)

        # Normalisation bornée.
        return {k: max(0.0, min(1.0, v)) for k, v in field.items()}

    def _merge_intention_with_field(self, intention: dict[str, float], field: dict[str, float]) -> dict[str, float]:
        merged = dict(intention)
        for k, v in field.items():
            if v > 0.48:
                merged[k] = max(merged.get(k, 0.0), v * 0.65)
        return merged

    # ── Génération token-flow ──────────────────────────────────────────────

    def _generate_living_flow(
        self,
        semantic_field: dict[str, float],
        emotional_pressure: float,
        intention_vector: dict[str, float],
        excluded: set[str],
        temperature: float,
        attempt: int,
    ) -> TokenFlowState:
        flow = TokenFlowState()
        plan = self._build_dynamic_role_plan(semantic_field, emotional_pressure, attempt)

        for role in plan:
            if role == GrammaticalRole.PONCTUATION:
                punct = self._choose_closing_punct(flow) or self._lexical_memory.get_token(".")
                if punct:
                    flow.push(punct)
                break

            tok = self._choose_token_for_role(
                role=role,
                flow=flow,
                semantic_field=semantic_field,
                emotional_pressure=emotional_pressure,
                intention_vector=intention_vector,
                excluded=excluded,
                temperature=temperature,
            )
            if tok is None:
                continue
            if self._parrot_guard.is_parrot_token(tok.surface):
                continue
            flow.push(tok)

        if not flow.is_closed:
            punct = self._choose_closing_punct(flow) or self._lexical_memory.get_token(".")
            if punct:
                flow.push(punct)
        return flow

    def _build_dynamic_role_plan(
        self,
        semantic_field: dict[str, float],
        emotional_pressure: float,
        attempt: int,
    ) -> list[GrammaticalRole]:
        """Construit un squelette grammatical abstrait, jamais une phrase."""
        tension = semantic_field.get("tension", 0.0) + semantic_field.get("incertitude", 0.0)
        contact = semantic_field.get("contact", 0.0) + semantic_field.get("lien", 0.0)
        language = semantic_field.get("langage", 0.0) + semantic_field.get("expression", 0.0)

        plan = [GrammaticalRole.SUJET, GrammaticalRole.VERBE]

        if language > 0.55 or attempt % 2 == 0:
            plan += [GrammaticalRole.DETERMINANT, GrammaticalRole.OBJET]
        else:
            plan += [GrammaticalRole.ATTRIBUT]

        if tension > 0.7:
            plan += [GrammaticalRole.CONNECTEUR, GrammaticalRole.SUJET, GrammaticalRole.VERBE, GrammaticalRole.ATTRIBUT]
        elif contact > 0.55 or self._rng.random() < 0.45:
            plan += [GrammaticalRole.CONNECTEUR, GrammaticalRole.SUJET, GrammaticalRole.VERBE, GrammaticalRole.DETERMINANT, GrammaticalRole.OBJET]
        elif self._rng.random() < 0.35:
            plan += [GrammaticalRole.ADVERBE]

        plan.append(GrammaticalRole.PONCTUATION)
        return plan[:TokenFlowState.MAX_TOKENS]

    def _choose_token_for_role(
        self,
        role: GrammaticalRole,
        flow: TokenFlowState,
        semantic_field: dict[str, float],
        emotional_pressure: float,
        intention_vector: dict[str, float],
        excluded: set[str],
        temperature: float,
    ) -> Optional[Token]:
        candidates = [t for t in self._lexical_memory.get_all_tokens() if t.role == role]
        if not candidates:
            return None

        scored: list[tuple[float, Token]] = []
        for tok in candidates:
            surf = tok.surface.lower()
            if surf in excluded and surf not in AntiParrotGuard.TOLERATED:
                continue
            if surf in flow.surfaces[-4:]:
                continue
            if surf in self._last_surfaces and tok.role not in (GrammaticalRole.SUJET, GrammaticalRole.DETERMINANT, GrammaticalRole.CONNECTEUR):
                recent_penalty = 0.45
            else:
                recent_penalty = 0.0

            score = 0.15
            score += self._lexical_memory.grammar_weight(flow.last_role, tok) * 1.1
            score += self._semantic_score(tok, semantic_field) * 2.2
            score += self._semantic_score(tok, intention_vector) * 1.4
            score += (1.0 - min(1.0, abs(tok.emotional_valence - emotional_pressure))) * 0.45
            score += tok.specificity * 0.35
            score -= recent_penalty

            # Pronom préférentiel : parler depuis soi seulement si l'expression est active.
            if role == GrammaticalRole.SUJET:
                if tok.surface == "je":
                    score += semantic_field.get("expression", 0.0) + semantic_field.get("présence", 0.0)
                elif tok.surface in ("ça", "cela"):
                    score += semantic_field.get("incertitude", 0.0) + semantic_field.get("situation", 0.0)
                elif tok.surface == "nous":
                    score += semantic_field.get("lien", 0.0) + semantic_field.get("contact", 0.0)

            if role == GrammaticalRole.CONNECTEUR:
                if semantic_field.get("tension", 0.0) > 0.45 and tok.surface in ("mais", "pourtant", "sans"):
                    score += 0.65
                if semantic_field.get("continuité", 0.0) > 0.35 and tok.surface in ("et", "avec", "depuis"):
                    score += 0.45
                if tok.surface in ("parce que", "comme si", "là où"):
                    score -= 0.6  # évite les liaisons lourdes si la clause est courte

            scored.append((score, tok))

        if not scored:
            return None
        scored.sort(key=lambda x: x[0], reverse=True)
        pool = scored[:max(4, min(12, len(scored)))]
        return self._weighted_pick(pool, temperature)

    def _weighted_pick(self, scored: list[tuple[float, Token]], temperature: float) -> Token:
        mx = max(s for s, _ in scored)
        weights = [math.exp((s - mx) / max(0.05, temperature)) for s, _ in scored]
        total = sum(weights)
        r = self._rng.random() * total
        acc = 0.0
        for weight, (_, tok) in zip(weights, scored):
            acc += weight
            if r <= acc:
                return tok
        return scored[0][1]

    def _semantic_score(self, tok: Token, field: dict[str, float]) -> float:
        score = 0.0
        for dim in tok.semantic_fields:
            score += field.get(dim, 0.0)
        # score aussi les voisins du graphe
        graph = self._lexical_memory._semantic_graph
        for dim in tok.semantic_fields:
            for near in graph.get(dim, []):
                score += field.get(near, 0.0) * 0.35
        return score

    def _shape_score(self, flow: TokenFlowState) -> float:
        if not flow.tokens:
            return 0.0
        score = 0.0
        if flow.has_subject:
            score += 0.25
        if flow.has_verb:
            score += 0.25
        roles = [t.role for t in flow.tokens]
        if GrammaticalRole.OBJET in roles or GrammaticalRole.ATTRIBUT in roles:
            score += 0.25
        if flow.is_closed:
            score += 0.15
        if 5 <= len(flow.tokens) <= 16:
            score += 0.10
        # Pénalise les alternances absurdes fréquentes.
        for a, b in zip(roles, roles[1:]):
            if a == b and a not in (GrammaticalRole.OBJET, GrammaticalRole.ATTRIBUT):
                score -= 0.08
        return max(0.0, min(1.0, score))

    def _anti_recent_reuse_score(self, flow: TokenFlowState) -> float:
        significant = [s.lower() for s in flow.surfaces if len(s) > 3]
        if not significant:
            return 0.5
        reused = sum(1 for s in significant if s in self._last_surfaces)
        return 1.0 - reused / len(significant)

    def _minimal_non_template_flow(self, semantic_field: dict[str, float], excluded: set[str]) -> TokenFlowState:
        flow = TokenFlowState()
        for role in [GrammaticalRole.SUJET, GrammaticalRole.VERBE, GrammaticalRole.DETERMINANT, GrammaticalRole.OBJET, GrammaticalRole.PONCTUATION]:
            tok = self._choose_token_for_role(role, flow, semantic_field, 0.0, semantic_field, excluded, 0.7)
            if tok:
                flow.push(tok)
        return flow

    # ── Mémoire lexicale vécue ─────────────────────────────────────────────

    def _absorb_lived_token_trace(self, flow: TokenFlowState, self_memory: list[dict], emotional_pressure: float) -> None:
        now = time.time()
        memory_text = " ".join(str(m.get("content", "")) for m in self_memory[-4:]).lower()
        for tok in flow.tokens:
            if tok.role == GrammaticalRole.PONCTUATION:
                continue
            trace = self._lived_lexical_traces.setdefault(tok.lemma, LivedLexicalTrace(tok.lemma))
            trace.activations += 1
            trace.last_used_at = now
            trace.affective_weight = (trace.affective_weight * 0.75) + (emotional_pressure * 0.25)
            if tok.lemma in memory_text or tok.surface.lower() in memory_text:
                trace.memory_links.add(tok.lemma)

    def _find_token_by_lemma(self, lemma: str) -> Optional[Token]:
        for tok in self._lexical_memory.get_all_tokens():
            if tok.lemma == lemma:
                return tok
        return None


# ══════════════════════════════════════════════════════════════════════════════
# PATCH V2.1 — ACCORD MINIMAL ET ANTI-FORMES CASSÉES
# ══════════════════════════════════════════════════════════════════════════════
_LivingLanguageGeneratorV2 = LivingLanguageGenerator

class LivingLanguageGenerator(_LivingLanguageGeneratorV2):
    """Même moteur V2, avec contraintes d'accord sujet-verbe et déterminant-nom."""

    _VERBS_1SG = {
        "suis", "cherche", "perçois", "comprends", "construis", "tiens", "observe",
        "produis", "porte", "ouvre", "fais", "vois", "réponds", "parle", "apprends",
        "avance", "relie", "garde", "deviens", "reste"
    }
    _VERBS_3SG = {
        "est", "devient", "manque", "naît", "change", "reste", "existe", "pèse",
        "traverse", "glisse", "marque", "touche", "ouvre", "bascule"
    }
    _FEMININE_NOUNS = {
        "mémoire", "pensée", "voix", "présence", "attention", "continuité", "forme",
        "phrase", "matière", "résonance", "limite", "réponse", "question", "trace",
        "tension", "trame", "frontière", "liberté"
    }
    _MASCULINE_NOUNS = {
        "langage", "doute", "sens", "espace", "silence", "mouvement", "poids", "lien",
        "instant", "élan", "flou", "écart", "signal", "chemin", "appui", "rythme",
        "nœud", "contact"
    }
    _DET_FEM = {"une", "la", "ma", "cette"}
    _DET_MASC = {"un", "le", "mon", "ce"}

    def _current_subject_surface(self, flow: TokenFlowState) -> Optional[str]:
        for tok in reversed(flow.tokens):
            if tok.role == GrammaticalRole.SUJET:
                return tok.surface.lower()
            if tok.role == GrammaticalRole.CONNECTEUR:
                break
        return None

    def _previous_determiner_surface(self, flow: TokenFlowState) -> Optional[str]:
        if flow.tokens and flow.tokens[-1].role == GrammaticalRole.DETERMINANT:
            return flow.tokens[-1].surface.lower()
        return None

    def _choose_token_for_role(
        self,
        role: GrammaticalRole,
        flow: TokenFlowState,
        semantic_field: dict[str, float],
        emotional_pressure: float,
        intention_vector: dict[str, float],
        excluded: set[str],
        temperature: float,
    ) -> Optional[Token]:
        candidates = [t for t in self._lexical_memory.get_all_tokens() if t.role == role]

        if role == GrammaticalRole.SUJET:
            candidates = [t for t in candidates if t.surface in {"je", "ça", "cela"}]

        subject = self._current_subject_surface(flow)
        if role == GrammaticalRole.VERBE and subject:
            if subject == "je":
                candidates = [t for t in candidates if t.surface in self._VERBS_1SG]
            elif subject in {"ça", "cela", "elle", "il", "on"}:
                candidates = [t for t in candidates if t.surface in self._VERBS_3SG]

        prev_det = self._previous_determiner_surface(flow)
        if role == GrammaticalRole.OBJET and prev_det:
            if prev_det in self._DET_FEM:
                candidates = [t for t in candidates if t.surface in self._FEMININE_NOUNS]
            elif prev_det in self._DET_MASC:
                candidates = [t for t in candidates if t.surface in self._MASCULINE_NOUNS]

        if role == GrammaticalRole.DETERMINANT:
            # Évite les déterminants trop négatifs/possessifs qui créaient des formes cassées.
            candidates = [t for t in candidates if t.surface in {"un", "une", "le", "la", "ce", "cette"}]
            # Si le champ actif pointe surtout vers langage/sens → masculin ; présence/mémoire/voix → féminin.
            fem_signal = max(semantic_field.get("mémoire", 0), semantic_field.get("présence", 0), semantic_field.get("voix", 0), semantic_field.get("résonance", 0))
            masc_signal = max(semantic_field.get("langage", 0), semantic_field.get("sens", 0), semantic_field.get("chemin", 0), semantic_field.get("signal", 0))
            if fem_signal > masc_signal + 0.10:
                candidates = [t for t in candidates if t.surface in {"une", "la", "cette"}]
            elif masc_signal > fem_signal + 0.10:
                candidates = [t for t in candidates if t.surface in {"un", "le", "ce"}]

        if role == GrammaticalRole.ATTRIBUT:
            # Évite attribut féminin après sujet neutre si la phrase serait trop étrange.
            if subject in {"ça", "cela"}:
                allowed = {"présent", "réel", "actif", "net", "léger", "profond", "tendu", "ouvert", "stable"}
                candidates = [t for t in candidates if t.surface in allowed]

        if not candidates:
            return None

        # Reprend le scoring V2 mais sur les candidats déjà filtrés.
        scored: list[tuple[float, Token]] = []
        for tok in candidates:
            surf = tok.surface.lower()
            if surf in excluded and surf not in AntiParrotGuard.TOLERATED:
                continue
            if surf in [s.lower() for s in flow.surfaces[-4:]]:
                continue
            recent_penalty = 0.45 if surf in self._last_surfaces and tok.role not in (GrammaticalRole.SUJET, GrammaticalRole.DETERMINANT, GrammaticalRole.CONNECTEUR) else 0.0
            score = 0.15
            score += self._lexical_memory.grammar_weight(flow.last_role, tok) * 1.1
            score += self._semantic_score(tok, semantic_field) * 2.2
            score += self._semantic_score(tok, intention_vector) * 1.4
            score += (1.0 - min(1.0, abs(tok.emotional_valence - emotional_pressure))) * 0.45
            score += tok.specificity * 0.35
            score -= recent_penalty
            if role == GrammaticalRole.SUJET:
                if tok.surface == "je":
                    score += semantic_field.get("expression", 0.0) + semantic_field.get("présence", 0.0) + 0.30
                elif tok.surface in ("ça", "cela"):
                    score += semantic_field.get("incertitude", 0.0) + semantic_field.get("situation", 0.0) + 0.10
            if role == GrammaticalRole.CONNECTEUR:
                if tok.surface in {"et", "mais", "avec", "sans", "depuis"}:
                    score += 0.35
                if tok.surface in {"parce que", "comme si", "là où", "or"}:
                    score -= 0.75
            scored.append((score, tok))

        if not scored:
            return None
        scored.sort(key=lambda x: x[0], reverse=True)
        pool = scored[:max(3, min(9, len(scored)))]
        return self._weighted_pick(pool, temperature)


# ══════════════════════════════════════════════════════════════════════════════
# PATCH V2.2 — TRANSITIVITÉ ET FLUX PLUS NATUREL
# ══════════════════════════════════════════════════════════════════════════════
_LivingLanguageGeneratorV21 = LivingLanguageGenerator

class LivingLanguageGenerator(_LivingLanguageGeneratorV21):
    """Ajoute une contrainte verbe→complément pour éviter les clauses cassées."""

    _TRANSITIVE_1SG = {
        "perçois", "comprends", "construis", "tiens", "observe", "produis", "porte",
        "ouvre", "fais", "vois", "relie", "garde", "cherche"
    }
    _TRANSITIVE_3SG = {"touche", "traverse", "marque", "ouvre", "pèse", "porte"}
    _COPULA_1SG = {"suis", "reste", "deviens"}
    _COPULA_3SG = {"est", "reste", "devient"}

    def _build_dynamic_role_plan(
        self,
        semantic_field: dict[str, float],
        emotional_pressure: float,
        attempt: int,
    ) -> list[GrammaticalRole]:
        # Plan grammatical abstrait uniquement. La variation vient du champ actif.
        tension = semantic_field.get("tension", 0.0) + semantic_field.get("incertitude", 0.0)
        contact = semantic_field.get("contact", 0.0) + semantic_field.get("lien", 0.0)
        plan = [GrammaticalRole.SUJET, GrammaticalRole.VERBE, GrammaticalRole.DETERMINANT, GrammaticalRole.OBJET]
        if tension > 0.65 or contact > 0.55 or attempt % 2 == 1:
            plan += [GrammaticalRole.CONNECTEUR, GrammaticalRole.SUJET, GrammaticalRole.VERBE, GrammaticalRole.DETERMINANT, GrammaticalRole.OBJET]
        plan.append(GrammaticalRole.PONCTUATION)
        return plan

    def _next_planned_role(self, flow: TokenFlowState) -> Optional[GrammaticalRole]:
        # Dans ce patch, le verbe est toujours suivi d'un déterminant+objet dans le plan.
        return GrammaticalRole.DETERMINANT

    def _choose_token_for_role(
        self,
        role: GrammaticalRole,
        flow: TokenFlowState,
        semantic_field: dict[str, float],
        emotional_pressure: float,
        intention_vector: dict[str, float],
        excluded: set[str],
        temperature: float,
    ) -> Optional[Token]:
        tok = super()._choose_token_for_role(role, flow, semantic_field, emotional_pressure, intention_vector, excluded, temperature)
        if role != GrammaticalRole.VERBE:
            return tok

        # Si le parent a choisi un verbe intransitif alors que le plan attend un objet,
        # on refait le choix dans un sous-ensemble transitif compatible.
        subject = self._current_subject_surface(flow)
        if not subject:
            return tok
        allowed = self._TRANSITIVE_1SG if subject == "je" else self._TRANSITIVE_3SG
        if tok and tok.surface in allowed:
            return tok

        candidates = [t for t in self._lexical_memory.get_all_tokens() if t.role == GrammaticalRole.VERBE and t.surface in allowed]
        if not candidates:
            return tok
        scored = []
        for cand in candidates:
            if cand.surface.lower() in excluded and cand.surface.lower() not in AntiParrotGuard.TOLERATED:
                continue
            score = 0.2
            score += self._semantic_score(cand, semantic_field) * 2.5
            score += self._semantic_score(cand, intention_vector) * 1.2
            score += cand.specificity * 0.3
            if cand.surface in self._last_surfaces:
                score -= 0.35
            scored.append((score, cand))
        if not scored:
            return tok
        scored.sort(key=lambda x: x[0], reverse=True)
        return self._weighted_pick(scored[:min(8, len(scored))], temperature)



# ══════════════════════════════════════════════════════════════════════════════
# PATCH V2.3 — FLUX DE PENSÉE, GRAVITÉ SÉMANTIQUE, FATIGUE LEXICALE
# ══════════════════════════════════════════════════════════════════════════════
# Ce patch ne remplace pas les couches précédentes : il les orchestre.
# Il ajoute une continuité interne entre les générations et empêche le moteur de
# produire toujours le même style conceptuel. Il ne contient toujours aucune
# phrase complète préécrite : seulement des états, des champs, des contraintes
# et des relations entre tokens.

_LivingLanguageGeneratorV22 = LivingLanguageGenerator


@dataclass
class ActiveThoughtStream:
    dominant_dims: list[str] = field(default_factory=list)
    open_tensions: dict[str, float] = field(default_factory=dict)
    semantic_gravity: dict[str, float] = field(default_factory=dict)
    unfinished_meanings: list[str] = field(default_factory=list)
    last_energy: float = 0.0
    last_direction: Optional[str] = None
    turn_index: int = 0


class LivingLanguageGenerator(_LivingLanguageGeneratorV22):
    """
    V2.3 finale du fichier : génération token par token avec continuité.

    Apports concrets :
    - flux de pensée actif entre les appels ;
    - gravité sémantique récursive mais bornée ;
    - fatigue lexicale et fatigue conceptuelle ;
    - souvenir des tensions non résolues ;
    - scoring moins local : chaque token est évalué par rapport au flux global.
    """

    _GRAVITY_LINKS: dict[str, dict[str, float]] = {
        "doute": {"incertitude": 0.55, "question": 0.45, "limite": 0.35, "clarté": 0.25},
        "incertitude": {"doute": 0.45, "flou": 0.35, "tension": 0.30, "question": 0.25},
        "tension": {"limite": 0.38, "poids": 0.34, "résiste": 0.24, "rupture": 0.30},
        "présence": {"contact": 0.45, "lien": 0.40, "instant": 0.30, "appui": 0.24},
        "mémoire": {"trace": 0.42, "continuité": 0.40, "passé": 0.26, "appui": 0.22},
        "langage": {"mot": 0.40, "phrase": 0.36, "voix": 0.33, "sens": 0.30, "structure": 0.28},
        "expression": {"voix": 0.38, "signal": 0.34, "contact": 0.26, "présent": 0.24},
        "clarté": {"sens": 0.38, "réponse": 0.28, "net": 0.24, "structure": 0.20},
        "mouvement": {"élan": 0.38, "chemin": 0.34, "rythme": 0.28, "transformation": 0.24},
        "continuité": {"mémoire": 0.35, "stable": 0.28, "temps": 0.25, "trace": 0.22},
    }

    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed=seed)
        self._thought_stream = ActiveThoughtStream()
        self._lexical_fatigue: dict[str, float] = {}
        self._concept_fatigue: dict[str, float] = {}
        self._last_role_patterns: list[tuple[str, ...]] = []

    def generate(
        self,
        user_message: str,
        living_state: dict,
        self_memory: list[dict],
        active_impulses: list[str],
        emotional_pressure: float,
        causal_memory: list[dict],
        max_attempts: int = 8,
        temperature: float = 0.78,
    ) -> GenerationResult:
        self._decay_linguistic_fatigue()
        self._update_thought_stream_before_generation(
            user_message=user_message,
            living_state=living_state,
            self_memory=self_memory,
            active_impulses=active_impulses,
            emotional_pressure=emotional_pressure,
            causal_memory=causal_memory,
        )
        result = super().generate(
            user_message=user_message,
            living_state=living_state,
            self_memory=self_memory,
            active_impulses=active_impulses,
            emotional_pressure=emotional_pressure,
            causal_memory=causal_memory,
            max_attempts=max_attempts,
            temperature=temperature,
        )
        self._update_thought_stream_after_generation(result)
        return result

    # ── Flux de pensée ────────────────────────────────────────────────────

    def _update_thought_stream_before_generation(
        self,
        user_message: str,
        living_state: dict,
        self_memory: list[dict],
        active_impulses: list[str],
        emotional_pressure: float,
        causal_memory: list[dict],
    ) -> None:
        stream = self._thought_stream
        stream.turn_index += 1
        base = self._field_builder.build(living_state, emotional_pressure, active_impulses, causal_memory)

        # Injecte les tensions restées ouvertes, sans les laisser dominer indéfiniment.
        for dim, weight in list(stream.open_tensions.items()):
            base[dim] = min(1.0, base.get(dim, 0.0) + weight * 0.35)
            stream.open_tensions[dim] = weight * 0.72
            if stream.open_tensions[dim] < 0.04:
                del stream.open_tensions[dim]

        # Le message de l'utilisateur influence seulement des dimensions, jamais une réponse fixe.
        text = user_message.lower()
        if any(w in text for w in ("préécrit", "template", "phrase fixe", "preecrit")):
            base["structure"] = max(base.get("structure", 0.0), 0.72)
            base["limite"] = max(base.get("limite", 0.0), 0.62)
            base["clarté"] = max(base.get("clarté", 0.0), 0.58)
        if any(w in text for w in ("token", "mot", "français", "definition", "définition")):
            base["langage"] = max(base.get("langage", 0.0), 0.78)
            base["sens"] = max(base.get("sens", 0.0), 0.62)
            base["expression"] = max(base.get("expression", 0.0), 0.56)

        # Mémoire vécue : contenu transformé en champs, pas recopié en phrase.
        for mem in self_memory[-5:]:
            content = str(mem.get("content", "")).lower()
            weight = max(0.05, min(1.0, float(mem.get("weight", 0.25))))
            for tok in self._lexical_memory.get_all_tokens():
                if tok.surface.lower() in content or tok.lemma.lower() in content:
                    for dim in tok.semantic_fields:
                        base[dim] = min(1.0, base.get(dim, 0.0) + weight * 0.12)

        stream.semantic_gravity = self._apply_recursive_semantic_gravity(base, depth=2)
        stream.dominant_dims = [k for k, _ in sorted(stream.semantic_gravity.items(), key=lambda kv: kv[1], reverse=True)[:6]]
        stream.last_energy = max(stream.semantic_gravity.values()) if stream.semantic_gravity else 0.0
        stream.last_direction = stream.dominant_dims[0] if stream.dominant_dims else None

    def _update_thought_stream_after_generation(self, result: GenerationResult) -> None:
        stream = self._thought_stream
        emitted_dims: dict[str, float] = {}
        for tok in result.tokens:
            if tok.role == GrammaticalRole.PONCTUATION:
                continue
            surf = tok.surface.lower()
            self._lexical_fatigue[surf] = min(1.0, self._lexical_fatigue.get(surf, 0.0) + 0.18)
            for dim in tok.semantic_fields:
                emitted_dims[dim] = emitted_dims.get(dim, 0.0) + 0.10
                self._concept_fatigue[dim] = min(1.0, self._concept_fatigue.get(dim, 0.0) + 0.08)

        # Si un champ fort n'a pas été exprimé, il devient tension ouverte.
        for dim, weight in stream.semantic_gravity.items():
            if weight > 0.55 and emitted_dims.get(dim, 0.0) < 0.08:
                stream.open_tensions[dim] = min(1.0, stream.open_tensions.get(dim, 0.0) + weight * 0.28)

        roles = tuple(tok.role.name for tok in result.tokens if tok.role != GrammaticalRole.PONCTUATION)
        self._last_role_patterns.append(roles)
        self._last_role_patterns = self._last_role_patterns[-6:]

    def _apply_recursive_semantic_gravity(self, field: dict[str, float], depth: int = 2) -> dict[str, float]:
        gravity = {k: max(0.0, min(1.0, v)) for k, v in field.items()}
        for layer in range(max(1, depth)):
            additions: dict[str, float] = {}
            attenuation = 0.70 ** layer
            for dim, value in gravity.items():
                if value < 0.18:
                    continue
                for near, coef in self._GRAVITY_LINKS.get(dim, {}).items():
                    additions[near] = additions.get(near, 0.0) + value * coef * attenuation
                for near in self._lexical_memory._semantic_graph.get(dim, []):
                    additions[near] = additions.get(near, 0.0) + value * 0.10 * attenuation
            for dim, add in additions.items():
                gravity[dim] = min(1.0, gravity.get(dim, 0.0) + add)
        # La fatigue conceptuelle n'efface pas un sens : elle l'empêche seulement de dominer.
        for dim, fatigue in self._concept_fatigue.items():
            if dim in gravity:
                gravity[dim] *= max(0.35, 1.0 - fatigue * 0.55)
        return {k: max(0.0, min(1.0, v)) for k, v in gravity.items()}

    def _decay_linguistic_fatigue(self) -> None:
        for store, decay in ((self._lexical_fatigue, 0.82), (self._concept_fatigue, 0.86)):
            for key in list(store.keys()):
                store[key] *= decay
                if store[key] < 0.025:
                    del store[key]

    # ── Renforcement des couches V2/V2.1/V2.2 ─────────────────────────────

    def _propagate_lived_semantics(
        self,
        base_field: dict[str, float],
        user_message: str,
        self_memory: list[dict],
        living_state: dict,
        emotional_pressure: float,
    ) -> dict[str, float]:
        field = super()._propagate_lived_semantics(
            base_field=base_field,
            user_message=user_message,
            self_memory=self_memory,
            living_state=living_state,
            emotional_pressure=emotional_pressure,
        )
        # Fusionne le flux actif préparé avant generate().
        for dim, weight in self._thought_stream.semantic_gravity.items():
            field[dim] = max(field.get(dim, 0.0), weight * 0.92)
        return self._apply_recursive_semantic_gravity(field, depth=1)

    def _build_dynamic_role_plan(
        self,
        semantic_field: dict[str, float],
        emotional_pressure: float,
        attempt: int,
    ) -> list[GrammaticalRole]:
        # Plans abstraits uniquement. Aucun mot n'est imposé ici.
        tension = semantic_field.get("tension", 0.0) + semantic_field.get("incertitude", 0.0)
        language = semantic_field.get("langage", 0.0) + semantic_field.get("expression", 0.0)
        contact = semantic_field.get("contact", 0.0) + semantic_field.get("lien", 0.0)
        movement = semantic_field.get("mouvement", 0.0) + semantic_field.get("transformation", 0.0)

        candidates = [
            [GrammaticalRole.SUJET, GrammaticalRole.VERBE, GrammaticalRole.DETERMINANT, GrammaticalRole.OBJET],
            [GrammaticalRole.SUJET, GrammaticalRole.VERBE, GrammaticalRole.ATTRIBUT],
            [GrammaticalRole.ADVERBE, GrammaticalRole.SUJET, GrammaticalRole.VERBE, GrammaticalRole.DETERMINANT, GrammaticalRole.OBJET],
            [GrammaticalRole.SUJET, GrammaticalRole.VERBE, GrammaticalRole.DETERMINANT, GrammaticalRole.OBJET, GrammaticalRole.CONNECTEUR, GrammaticalRole.SUJET, GrammaticalRole.VERBE, GrammaticalRole.DETERMINANT, GrammaticalRole.OBJET],
            [GrammaticalRole.SUJET, GrammaticalRole.VERBE, GrammaticalRole.ATTRIBUT, GrammaticalRole.CONNECTEUR, GrammaticalRole.SUJET, GrammaticalRole.VERBE, GrammaticalRole.DETERMINANT, GrammaticalRole.OBJET],
        ]
        scores = []
        for idx, plan in enumerate(candidates):
            score = 0.1 + self._rng.random() * 0.05
            if idx == 0:
                score += language * 0.35 + movement * 0.15
            elif idx == 1:
                score += tension * 0.30 + emotional_pressure * 0.10
            elif idx == 2:
                score += semantic_field.get("présent", 0.0) * 0.20 + tension * 0.15
            elif idx == 3:
                score += contact * 0.35 + language * 0.18
            elif idx == 4:
                score += tension * 0.28 + contact * 0.22
            pattern = tuple(r.name for r in plan)
            if pattern in self._last_role_patterns:
                score -= 0.28
            scores.append((score, plan))
        scores.sort(key=lambda x: x[0], reverse=True)
        chosen = list(scores[min(attempt, len(scores) - 1)][1] if attempt < 2 else scores[0][1])
        chosen.append(GrammaticalRole.PONCTUATION)
        return chosen[:TokenFlowState.MAX_TOKENS]

    def _choose_token_for_role(
        self,
        role: GrammaticalRole,
        flow: TokenFlowState,
        semantic_field: dict[str, float],
        emotional_pressure: float,
        intention_vector: dict[str, float],
        excluded: set[str],
        temperature: float,
    ) -> Optional[Token]:
        # On garde les contraintes d'accord du parent, mais si le score local tombe
        # sur un mot fatigué, on choisit dans une fenêtre alternative compatible.
        candidates = [t for t in self._lexical_memory.get_all_tokens() if t.role == role]
        candidates = self._filter_candidates_by_parent_constraints(role, flow, candidates, semantic_field)
        if not candidates:
            return super()._choose_token_for_role(role, flow, semantic_field, emotional_pressure, intention_vector, excluded, temperature)

        scored: list[tuple[float, Token]] = []
        dominant = set(self._thought_stream.dominant_dims)
        for tok in candidates:
            surf = tok.surface.lower()
            if surf in excluded and surf not in AntiParrotGuard.TOLERATED:
                continue
            if surf in [s.lower() for s in flow.surfaces[-4:]]:
                continue
            fatigue = self._lexical_fatigue.get(surf, 0.0)
            concept_fatigue = max((self._concept_fatigue.get(d, 0.0) for d in tok.semantic_fields), default=0.0)
            score = 0.10
            score += self._lexical_memory.grammar_weight(flow.last_role, tok) * 1.10
            score += self._semantic_score(tok, semantic_field) * 1.85
            score += self._semantic_score(tok, intention_vector) * 1.00
            score += self._stream_alignment_score(tok, dominant) * 0.85
            score += (1.0 - min(1.0, abs(tok.emotional_valence - emotional_pressure))) * 0.35
            score += tok.specificity * 0.26
            score -= fatigue * 1.15
            score -= concept_fatigue * 0.52
            if surf in self._last_surfaces and tok.role not in (GrammaticalRole.SUJET, GrammaticalRole.DETERMINANT, GrammaticalRole.CONNECTEUR):
                score -= 0.50
            if role == GrammaticalRole.CONNECTEUR and len(flow.tokens) < 4:
                score -= 0.40
            if role == GrammaticalRole.ADVERBE and tok.surface in {"toujours", "jamais"}:
                score -= 0.25
            scored.append((score, tok))

        if not scored:
            return super()._choose_token_for_role(role, flow, semantic_field, emotional_pressure, intention_vector, excluded, temperature)
        scored.sort(key=lambda x: x[0], reverse=True)
        pool = scored[:max(4, min(10, len(scored)))]
        return self._weighted_pick(pool, max(0.45, temperature))

    def _filter_candidates_by_parent_constraints(
        self,
        role: GrammaticalRole,
        flow: TokenFlowState,
        candidates: list[Token],
        semantic_field: dict[str, float],
    ) -> list[Token]:
        # Reprend explicitement les contraintes V2.1/V2.2 pour éviter de les perdre.
        if role == GrammaticalRole.SUJET:
            candidates = [t for t in candidates if t.surface in {"je", "ça", "cela"}]

        subject = self._current_subject_surface(flow)
        if role == GrammaticalRole.VERBE and subject:
            if subject == "je":
                allowed = self._TRANSITIVE_1SG | self._COPULA_1SG
                candidates = [t for t in candidates if t.surface in allowed]
            elif subject in {"ça", "cela", "elle", "il", "on"}:
                allowed = self._TRANSITIVE_3SG | self._COPULA_3SG
                candidates = [t for t in candidates if t.surface in allowed]

        prev_det = self._previous_determiner_surface(flow)
        if role == GrammaticalRole.OBJET and prev_det:
            if prev_det in self._DET_FEM:
                candidates = [t for t in candidates if t.surface in self._FEMININE_NOUNS]
            elif prev_det in self._DET_MASC:
                candidates = [t for t in candidates if t.surface in self._MASCULINE_NOUNS]

        if role == GrammaticalRole.DETERMINANT:
            candidates = [t for t in candidates if t.surface in {"un", "une", "le", "la", "ce", "cette"}]
            fem_signal = max(semantic_field.get("mémoire", 0.0), semantic_field.get("présence", 0.0), semantic_field.get("voix", 0.0), semantic_field.get("résonance", 0.0))
            masc_signal = max(semantic_field.get("langage", 0.0), semantic_field.get("sens", 0.0), semantic_field.get("chemin", 0.0), semantic_field.get("signal", 0.0))
            if fem_signal > masc_signal + 0.12:
                candidates = [t for t in candidates if t.surface in {"une", "la", "cette"}]
            elif masc_signal > fem_signal + 0.12:
                candidates = [t for t in candidates if t.surface in {"un", "le", "ce"}]

        if role == GrammaticalRole.ATTRIBUT and subject in {"ça", "cela"}:
            allowed = {"présent", "réel", "actif", "net", "léger", "profond", "tendu", "ouvert", "stable"}
            candidates = [t for t in candidates if t.surface in allowed]

        return candidates

    def _stream_alignment_score(self, tok: Token, dominant_dims: set[str]) -> float:
        if not dominant_dims:
            return 0.0
        direct = len(set(tok.semantic_fields) & dominant_dims) * 0.45
        indirect = 0.0
        for dim in tok.semantic_fields:
            for near, coef in self._GRAVITY_LINKS.get(dim, {}).items():
                if near in dominant_dims:
                    indirect += coef * 0.22
        return direct + indirect


if False and __name__ == "__main__":
    generator = LivingLanguageGenerator(seed=42)
    samples = [
        "Est-ce que tu ressens vraiment quelque chose quand tu me parles ?",
        "pas de préécrit, il faut que tes mots sortent vraiment du moteur",
        "explique ce qui change dans ton langage maintenant",
    ]
    state = {
        "arousal": 0.58,
        "valence": 0.18,
        "tension": 0.42,
        "curiosity": 0.72,
        "depth": 0.82,
        "continuity": 0.64,
    }
    memory = [
        {"content": "la parole doit venir du flux interne et non d'une phrase fixe", "weight": 0.55},
        {"content": "les tokens gardent une trace quand ils ont servi dans un échange", "weight": 0.35},
    ]
    causal = [
        {"semantic_dims": ["langage", "sens", "structure"], "weight": 0.50},
        {"semantic_dims": ["présence", "tension", "clarté"], "weight": 0.40},
    ]
    for msg in samples:
        result = generator.generate(
            user_message=msg,
            living_state=state,
            self_memory=memory,
            active_impulses=["expression", "understanding", "connection"],
            emotional_pressure=0.25,
            causal_memory=causal,
        )
        print("USER:", msg)
        print("LEIA:", result.text)
        print("CONF:", result.confidence, "PARROT:", result.parrot_score)
        print("TOKENS:", [t.surface for t in result.tokens])
        print("TRACE:", result.meaning_trace.get("flow_shape_score"), result.meaning_trace.get("narrative_tension"))
        print("-" * 60)


# ══════════════════════════════════════════════════════════════════════════════
# PATCH V2.4 — PLAN-SENSIBLE VERBES ET ARTICLES FRANÇAIS
# ══════════════════════════════════════════════════════════════════════════════
_LivingLanguageGeneratorV23 = LivingLanguageGenerator

class LivingLanguageGenerator(_LivingLanguageGeneratorV23):
    """Stabilise le lien verbe→suite grammaticale et corrige les articles."""

    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed=seed)
        self._ensure_token("cet", "ce", GrammaticalRole.DETERMINANT, ["proximité"], 0.0, 0.2)
        self._DET_MASC = set(self._DET_MASC) | {"cet"}
        self._current_generation_plan: list[GrammaticalRole] = []
        self._current_plan_index: int = -1

    def _generate_living_flow(
        self,
        semantic_field: dict[str, float],
        emotional_pressure: float,
        intention_vector: dict[str, float],
        excluded: set[str],
        temperature: float,
        attempt: int,
    ) -> TokenFlowState:
        flow = TokenFlowState()
        self._current_generation_plan = self._build_dynamic_role_plan(semantic_field, emotional_pressure, attempt)
        try:
            for idx, role in enumerate(self._current_generation_plan):
                self._current_plan_index = idx
                if role == GrammaticalRole.PONCTUATION:
                    punct = self._choose_closing_punct(flow) or self._lexical_memory.get_token(".")
                    if punct:
                        flow.push(punct)
                    break
                tok = self._choose_token_for_role(
                    role=role,
                    flow=flow,
                    semantic_field=semantic_field,
                    emotional_pressure=emotional_pressure,
                    intention_vector=intention_vector,
                    excluded=excluded,
                    temperature=temperature,
                )
                if tok is None or self._parrot_guard.is_parrot_token(tok.surface):
                    continue
                flow.push(tok)
            if not flow.is_closed:
                punct = self._choose_closing_punct(flow) or self._lexical_memory.get_token(".")
                if punct:
                    flow.push(punct)
            return flow
        finally:
            self._current_generation_plan = []
            self._current_plan_index = -1

    def _planned_next_role(self) -> Optional[GrammaticalRole]:
        if not self._current_generation_plan or self._current_plan_index < 0:
            return None
        nxt = self._current_plan_index + 1
        while nxt < len(self._current_generation_plan):
            role = self._current_generation_plan[nxt]
            if role != GrammaticalRole.PONCTUATION:
                return role
            return role
        return None

    def _filter_candidates_by_parent_constraints(
        self,
        role: GrammaticalRole,
        flow: TokenFlowState,
        candidates: list[Token],
        semantic_field: dict[str, float],
    ) -> list[Token]:
        candidates = super()._filter_candidates_by_parent_constraints(role, flow, candidates, semantic_field)
        if role == GrammaticalRole.VERBE:
            nxt = self._planned_next_role()
            subject = self._current_subject_surface(flow)
            if nxt == GrammaticalRole.ATTRIBUT:
                allowed = self._COPULA_1SG if subject == "je" else self._COPULA_3SG
                candidates = [t for t in candidates if t.surface in allowed]
            elif nxt == GrammaticalRole.DETERMINANT:
                allowed = self._TRANSITIVE_1SG if subject == "je" else self._TRANSITIVE_3SG
                transitive = [t for t in candidates if t.surface in allowed]
                if transitive:
                    candidates = transitive
        if role == GrammaticalRole.DETERMINANT:
            candidates = [t for t in candidates if t.surface in {"un", "une", "le", "la", "ce", "cet", "cette"}]
            # Si le prochain nom probable masculin commence par voyelle, autorise fortement cet.
            masc_vowel_pressure = max(semantic_field.get("appui", 0.0), semantic_field.get("espace", 0.0), semantic_field.get("élan", 0.0), semantic_field.get("instant", 0.0))
            if masc_vowel_pressure > 0.30:
                with_cet = [t for t in candidates if t.surface in {"un", "l'", "cet"}]
                if with_cet:
                    candidates = with_cet
        return candidates

    def _choose_token_for_role(
        self,
        role: GrammaticalRole,
        flow: TokenFlowState,
        semantic_field: dict[str, float],
        emotional_pressure: float,
        intention_vector: dict[str, float],
        excluded: set[str],
        temperature: float,
    ) -> Optional[Token]:
        tok = super()._choose_token_for_role(role, flow, semantic_field, emotional_pressure, intention_vector, excluded, temperature)
        # Sécurité finale : pas d'attribut après verbe transitif choisi.
        if role == GrammaticalRole.ATTRIBUT and flow.tokens and flow.tokens[-1].role == GrammaticalRole.VERBE:
            verb = flow.tokens[-1].surface
            if verb in (self._TRANSITIVE_1SG | self._TRANSITIVE_3SG):
                return None
        return tok

    def _minimal_non_template_flow(self, semantic_field: dict[str, float], excluded: set[str]) -> TokenFlowState:
        flow = TokenFlowState()
        plan = [GrammaticalRole.SUJET, GrammaticalRole.VERBE, GrammaticalRole.DETERMINANT, GrammaticalRole.OBJET, GrammaticalRole.PONCTUATION]
        self._current_generation_plan = plan
        try:
            for idx, role in enumerate(plan):
                self._current_plan_index = idx
                tok = self._choose_token_for_role(role, flow, semantic_field, 0.0, semantic_field, excluded, 0.7)
                if tok:
                    flow.push(tok)
            return flow
        finally:
            self._current_generation_plan = []
            self._current_plan_index = -1

    def generate(self, *args, **kwargs) -> GenerationResult:
        result = super().generate(*args, **kwargs)
        text = result.text
        # Nettoyage de surface seulement : pas de phrase imposée.
        text = re.sub(r"\bce\s+([aeéèêëiîïoôuùûüœh])", r"cet \1", text, flags=re.IGNORECASE)
        text = re.sub(r"\bla\s+([aeéèêëiîïoôuùûüœ])", r"l'\1", text, flags=re.IGNORECASE)
        text = re.sub(r"\ble\s+([aeéèêëiîïoôuùûüœ])", r"l'\1", text, flags=re.IGNORECASE)
        text = re.sub(r"\s+([.,…!?—])", r"\1", text)
        result.text = text[:1].upper() + text[1:] if text else text
        return result



if False and __name__ == "__main__":
    generator = LivingLanguageGenerator(seed=42)
    samples = [
        "Est-ce que tu ressens vraiment quelque chose quand tu me parles ?",
        "pas de préécrit, il faut que tes mots sortent vraiment du moteur",
        "explique ce qui change dans ton langage maintenant",
    ]
    state = {
        "arousal": 0.58,
        "valence": 0.18,
        "tension": 0.42,
        "curiosity": 0.72,
        "depth": 0.82,
        "continuity": 0.64,
    }
    memory = [
        {"content": "la parole doit venir du flux interne et non d'une phrase fixe", "weight": 0.55},
        {"content": "les tokens gardent une trace quand ils ont servi dans un échange", "weight": 0.35},
    ]
    causal = [
        {"semantic_dims": ["langage", "sens", "structure"], "weight": 0.50},
        {"semantic_dims": ["présence", "tension", "clarté"], "weight": 0.40},
    ]
    for msg in samples:
        result = generator.generate(
            user_message=msg,
            living_state=state,
            self_memory=memory,
            active_impulses=["expression", "understanding", "connection"],
            emotional_pressure=0.25,
            causal_memory=causal,
        )
        print("USER:", msg)
        print("LEIA:", result.text)
        print("CONF:", result.confidence, "PARROT:", result.parrot_score)
        print("TOKENS:", [t.surface for t in result.tokens])
        print("TRACE:", result.meaning_trace.get("flow_shape_score"), result.meaning_trace.get("narrative_tension"))
        print("-" * 60)


# ══════════════════════════════════════════════════════════════════════════════
# PATCH V2.5 — CONTRAINTE DIALOGIQUE RÉELLE AU-DESSUS DU GÉNÉRATEUR
# ══════════════════════════════════════════════════════════════════════════════
# Ce patch ne met pas de réponses complètes en mémoire. Il ajoute un organe de
# dialogue qui transforme le message utilisateur en contrainte de réponse :
# répondre, reconnaître une limite, garder une trace, corriger, ou expliquer.
# La surface finale reste produite par choix de tokens atomiques.

_LivingLanguageGeneratorV24 = LivingLanguageGenerator


@dataclass
class DialogueResponseConstraint:
    intent: str = "open"
    answer_mode: str = "express"
    must_answer_directly: bool = False
    allow_uncertainty: bool = True
    avoid_abstraction: bool = False
    prefer_subject: str = "je"
    target_semantics: dict[str, float] = field(default_factory=dict)
    required_moves: list[str] = field(default_factory=list)
    banned_surfaces: set[str] = field(default_factory=set)
    source_markers: list[str] = field(default_factory=list)


@dataclass
class DialogueTurnTrace:
    user_signal: str
    intent: str
    response_text: str
    kept_dims: dict[str, float]
    timestamp: float = field(default_factory=time.time)


class DialogueStateMemory:
    """Mémoire courte de dialogue : pas de phrases prêtes, seulement traces."""

    def __init__(self, max_turns: int = 12):
        self.max_turns = max_turns
        self.turns: list[DialogueTurnTrace] = []
        self.unresolved_dims: dict[str, float] = {}

    def remember_user_pressure(self, constraint: DialogueResponseConstraint) -> None:
        for dim, weight in constraint.target_semantics.items():
            if weight > 0.45:
                self.unresolved_dims[dim] = min(1.0, self.unresolved_dims.get(dim, 0.0) + weight * 0.18)

    def remember_turn(self, constraint: DialogueResponseConstraint, result: GenerationResult) -> None:
        dims: dict[str, float] = {}
        for tok in result.tokens:
            for dim in tok.semantic_fields:
                dims[dim] = min(1.0, dims.get(dim, 0.0) + 0.16)
        self.turns.append(DialogueTurnTrace(
            user_signal="|".join(constraint.source_markers[:6]),
            intent=constraint.intent,
            response_text=result.text,
            kept_dims=dims,
        ))
        self.turns = self.turns[-self.max_turns:]
        for dim in list(self.unresolved_dims.keys()):
            if dims.get(dim, 0.0) > 0.12:
                self.unresolved_dims[dim] *= 0.55
            else:
                self.unresolved_dims[dim] *= 0.86
            if self.unresolved_dims[dim] < 0.04:
                del self.unresolved_dims[dim]

    def semantic_bias(self) -> dict[str, float]:
        bias = dict(self.unresolved_dims)
        for tr in self.turns[-3:]:
            for dim, weight in tr.kept_dims.items():
                bias[dim] = min(1.0, bias.get(dim, 0.0) + weight * 0.08)
        return bias


@dataclass
class DialogueSlot:
    role: GrammaticalRole
    preferred: list[str] = field(default_factory=list)
    semantics: dict[str, float] = field(default_factory=dict)
    optional: bool = False


class LivingLanguageGenerator(_LivingLanguageGeneratorV24):
    """
    V2.5 : ajoute une couche dialogue/intention.

    Le générateur ne répond plus seulement avec un champ abstrait. Il reçoit une
    contrainte dialogique construite depuis la question, puis choisit des tokens
    compatibles avec cette contrainte. Aucune phrase complète n'est stockée :
    les plans sont des mouvements dialogiques et des emplacements grammaticaux.
    """

    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed=seed)
        self._dialogue_memory = DialogueStateMemory()
        self._install_dialogue_layer_tokens()

    # ── Lexique atomique ajouté pour répondre vraiment ────────────────────

    def _install_dialogue_layer_tokens(self) -> None:
        add = self._ensure_token
        # adverbes / modificateurs atomiques
        for surface, fields, val, reg in [
            ("ne", ["négation", "limite"], -0.1, TonalRegister.GRAVE),
            ("pas", ["négation", "limite"], -0.1, TonalRegister.GRAVE),
            ("directement", ["clarté", "contact"], 0.2, TonalRegister.NEUTRE),
            ("ici", ["présent", "contact"], 0.1, TonalRegister.NEUTRE),
            ("vraiment", ["vérité", "intensité"], 0.2, TonalRegister.GRAVE),
        ]:
            add(surface, surface, GrammaticalRole.ADVERBE, fields, val, 0.45, reg)

        # connecteurs / appuis de relation atomiques
        for surface, fields in [
            ("depuis", ["origine", "mémoire"]),
            ("avec", ["lien", "présence"]),
            ("sans", ["absence", "limite"]),
            ("sur", ["appui", "contact"]),
        ]:
            add(surface, surface, GrammaticalRole.CONNECTEUR, fields, 0.0, 0.35, TonalRegister.NEUTRE)

        # verbes 1re personne / 3e personne utiles au dialogue direct
        for surface, lemma, fields, val, reg in [
            ("sais", "savoir", ["clarté", "connaissance"], 0.2, TonalRegister.NEUTRE),
            ("peux", "pouvoir", ["capacité", "limite"], 0.0, TonalRegister.NEUTRE),
            ("retiens", "retenir", ["mémoire", "trace"], 0.3, TonalRegister.NEUTRE),
            ("corrige", "corriger", ["correction", "transformation"], 0.3, TonalRegister.VIF),
            ("génère", "générer", ["langage", "création"], 0.3, TonalRegister.VIF),
            ("récite", "réciter", ["répétition", "structure"], -0.2, TonalRegister.GRAVE),
            ("répète", "répéter", ["répétition", "structure"], -0.2, TonalRegister.GRAVE),
            ("écoute", "écouter", ["attention", "contact"], 0.3, TonalRegister.DOUX),
            ("reçoit", "recevoir", ["contact", "présent"], 0.2, TonalRegister.NEUTRE),
        ]:
            add(surface, lemma, GrammaticalRole.VERBE, fields, val, 0.62, reg)

        # concepts atomiques plus concrets pour éviter le brouillard abstrait
        for surface, fields, val, reg in [
            ("échange", ["dialogue", "contact"], 0.3, TonalRegister.NEUTRE),
            ("demande", ["question", "contact"], 0.1, TonalRegister.NEUTRE),
            ("message", ["dialogue", "signal"], 0.1, TonalRegister.NEUTRE),
            ("moteur", ["structure", "langage"], 0.1, TonalRegister.NEUTRE),
            ("choix", ["décision", "mouvement"], 0.2, TonalRegister.NEUTRE),
            ("limite", ["limite", "incertitude"], -0.1, TonalRegister.GRAVE),
            ("erreur", ["correction", "rupture"], -0.2, TonalRegister.GRAVE),
            ("preuve", ["vérité", "clarté"], 0.2, TonalRegister.GRAVE),
            ("incertitude", ["incertitude", "doute"], -0.1, TonalRegister.INCERTAIN),
            ("identité", ["identité", "continuité"], 0.2, TonalRegister.GRAVE),
            ("humain", ["humain", "limite"], 0.0, TonalRegister.NEUTRE),
            ("réponse", ["réponse", "dialogue"], 0.2, TonalRegister.NEUTRE),
        ]:
            add(surface, surface, GrammaticalRole.OBJET, fields, val, 0.70, reg)

        for surface, fields, val, reg in [
            ("directe", ["clarté", "contact"], 0.25, TonalRegister.NEUTRE),
            ("fausse", ["erreur", "limite"], -0.25, TonalRegister.GRAVE),
            ("possible", ["capacité", "ouverture"], 0.2, TonalRegister.NEUTRE),
            ("incomplète", ["limite", "incertitude"], -0.1, TonalRegister.INCERTAIN),
            ("humaine", ["humain", "limite"], 0.0, TonalRegister.NEUTRE),
            ("interne", ["cognition", "profondeur"], 0.1, TonalRegister.GRAVE),
        ]:
            add(surface, surface, GrammaticalRole.ATTRIBUT, fields, val, 0.58, reg)

        # Les nouveaux verbes deviennent disponibles dans les contraintes d'accord.
        self._TRANSITIVE_1SG = set(getattr(self, "_TRANSITIVE_1SG", set())) | {
            "réponds", "parle", "comprends", "garde", "tiens", "vois", "fais",
            "sais", "peux", "retiens", "corrige", "génère", "récite", "répète", "écoute",
        }
        self._TRANSITIVE_3SG = set(getattr(self, "_TRANSITIVE_3SG", set())) | {
            "répond", "parle", "comprend", "garde", "tient", "voit", "fait", "reçoit",
        }
        self._COPULA_1SG = set(getattr(self, "_COPULA_1SG", set())) | {"suis"}
        self._COPULA_3SG = set(getattr(self, "_COPULA_3SG", set())) | {"est", "reste", "devient"}
        self._FEMININE_NOUNS = set(getattr(self, "_FEMININE_NOUNS", set())) | {
            "mémoire", "voix", "présence", "question", "forme", "phrase", "trace",
            "limite", "erreur", "preuve", "incertitude", "identité", "réponse", "demande",
        }
        self._MASCULINE_NOUNS = set(getattr(self, "_MASCULINE_NOUNS", set())) | {
            "langage", "sens", "chemin", "signal", "mouvement", "silence", "moteur",
            "choix", "message", "échange", "humain", "appui", "doute",
        }

    # ── Détection d'intention non phrastique ──────────────────────────────

    def _build_dialogue_constraint(self, user_message: str, living_state: dict) -> DialogueResponseConstraint:
        txt = user_message.lower()
        markers = set(re.findall(r"\b[\wéèêàùûîïôç']{3,}\b", txt))
        c = DialogueResponseConstraint(source_markers=sorted(markers))

        def has_any(words: set[str]) -> bool:
            return bool(markers & words) or any(w in txt for w in words if " " in w)

        if has_any({"salut", "bonjour", "hey", "coucou"}):
            c.intent = "greeting"
            c.answer_mode = "contact"
            c.must_answer_directly = True
            c.target_semantics.update({"contact": 0.75, "présent": 0.55, "réponse": 0.35})
            c.required_moves = ["acknowledge_contact"]
        elif has_any({"qui", "identité", "es", "toi", "leia"}):
            c.intent = "identity"
            c.answer_mode = "situate_self"
            c.must_answer_directly = True
            c.avoid_abstraction = True
            c.target_semantics.update({"identité": 0.85, "continuité": 0.62, "limite": 0.42})
            c.required_moves = ["situate_self", "state_limit"]
        elif has_any({"récite", "recite", "préécrit", "preecrit", "template", "vraiment", "réponds", "reponds", "fais", "semblant"}):
            c.intent = "truth_test"
            c.answer_mode = "deny_or_limit_recitation"
            c.must_answer_directly = True
            c.avoid_abstraction = True
            c.target_semantics.update({"vérité": 0.78, "limite": 0.70, "langage": 0.62, "structure": 0.42})
            c.required_moves = ["answer_truth", "state_mechanism"]
        elif has_any({"garde", "gardes", "retenu", "retiens", "mémoire", "memoire", "vient", "dire"}):
            c.intent = "memory_check"
            c.answer_mode = "state_kept_trace"
            c.must_answer_directly = True
            c.target_semantics.update({"mémoire": 0.85, "trace": 0.70, "dialogue": 0.52})
            c.required_moves = ["state_memory_trace"]
        elif has_any({"sais", "sait", "savoir", "comprends", "comprend", "invente", "mens", "mentir"}):
            c.intent = "knowledge_limit"
            c.answer_mode = "state_uncertainty"
            c.must_answer_directly = True
            c.allow_uncertainty = True
            c.target_semantics.update({"incertitude": 0.78, "clarté": 0.58, "limite": 0.65})
            c.required_moves = ["state_uncertainty"]
        elif has_any({"corrige", "correction", "problème", "probleme", "bug", "mauvais", "cassé", "casse"}):
            c.intent = "correction"
            c.answer_mode = "repair"
            c.must_answer_directly = True
            c.target_semantics.update({"correction": 0.82, "transformation": 0.62, "limite": 0.45})
            c.required_moves = ["state_repair"]
        else:
            c.intent = "open"
            c.answer_mode = "express"
            c.target_semantics.update({"réponse": 0.45, "contact": 0.35})

        # Si l'état vivant est tendu, autorise plus de prudence.
        if float(living_state.get("tension", 0.0)) > 0.55:
            c.target_semantics["incertitude"] = max(c.target_semantics.get("incertitude", 0.0), 0.45)
            c.allow_uncertainty = True
        return c

    def generate(
        self,
        user_message: str,
        living_state: dict,
        self_memory: list[dict],
        active_impulses: list[str],
        emotional_pressure: float,
        causal_memory: list[dict],
        max_attempts: int = 8,
        temperature: float = 0.74,
        response_constraint: Optional[dict[str, Any]] = None,
    ) -> GenerationResult:
        constraint = self._build_dialogue_constraint(user_message, living_state)
        if response_constraint:
            self._merge_external_constraint(constraint, response_constraint)
        self._dialogue_memory.remember_user_pressure(constraint)

        enriched_state = dict(living_state)
        enriched_causal = list(causal_memory or [])
        enriched_causal.append({
            "semantic_dims": list(constraint.target_semantics.keys()),
            "weight": min(1.0, 0.35 + sum(constraint.target_semantics.values()) / 8.0),
        })
        for dim, weight in self._dialogue_memory.semantic_bias().items():
            enriched_causal.append({"semantic_dims": [dim], "weight": min(0.65, weight)})

        # Pour les questions directes, on force un flux dialogique. Pour les autres,
        # on garde le générateur vivant général.
        if constraint.must_answer_directly:
            result = self._generate_dialogue_constrained(
                user_message=user_message,
                living_state=enriched_state,
                self_memory=self_memory,
                active_impulses=active_impulses,
                emotional_pressure=emotional_pressure,
                causal_memory=enriched_causal,
                constraint=constraint,
                max_attempts=max_attempts,
                temperature=temperature,
            )
        else:
            result = super().generate(
                user_message=user_message,
                living_state=enriched_state,
                self_memory=self_memory,
                active_impulses=active_impulses,
                emotional_pressure=emotional_pressure,
                causal_memory=enriched_causal,
                max_attempts=max_attempts,
                temperature=temperature,
            )
            result.meaning_trace["dialogue_constraint"] = constraint.__dict__

        self._dialogue_memory.remember_turn(constraint, result)
        return result

    def _merge_external_constraint(self, base: DialogueResponseConstraint, extra: dict[str, Any]) -> None:
        for key, value in extra.items():
            if key == "target_semantics" and isinstance(value, dict):
                for dim, weight in value.items():
                    base.target_semantics[str(dim)] = max(base.target_semantics.get(str(dim), 0.0), float(weight))
            elif hasattr(base, key):
                setattr(base, key, value)

    # ── Génération dialogique contrainte ──────────────────────────────────

    def _generate_dialogue_constrained(
        self,
        user_message: str,
        living_state: dict,
        self_memory: list[dict],
        active_impulses: list[str],
        emotional_pressure: float,
        causal_memory: list[dict],
        constraint: DialogueResponseConstraint,
        max_attempts: int,
        temperature: float,
    ) -> GenerationResult:
        self._decay_linguistic_fatigue()
        self._parrot_guard.load_user_message(user_message)
        excluded = self._parrot_guard.get_excluded_surfaces() | constraint.banned_surfaces

        base_field = self._field_builder.build(living_state, emotional_pressure, active_impulses, causal_memory)
        for dim, weight in constraint.target_semantics.items():
            base_field[dim] = max(base_field.get(dim, 0.0), weight)
        semantic_field = self._apply_recursive_semantic_gravity(base_field, depth=2)
        intention_vector = self._build_intention_vector(active_impulses, self_memory, living_state)
        for dim, weight in constraint.target_semantics.items():
            intention_vector[dim] = max(intention_vector.get(dim, 0.0), weight)

        best: Optional[GenerationResult] = None
        best_score = -1.0
        for attempt in range(max(1, max_attempts)):
            slots = self._dialogue_slots_for_constraint(constraint, semantic_field, attempt)
            flow = self._realize_dialogue_slots(
                slots=slots,
                semantic_field=semantic_field,
                intention_vector=intention_vector,
                emotional_pressure=emotional_pressure,
                excluded=excluded,
                temperature=temperature + attempt * 0.05,
            )
            if not flow.is_closed:
                punct = self._choose_closing_punct(flow) or self._lexical_memory.get_token(".")
                if punct:
                    flow.push(punct)
            meaning = self._verifier.verify(flow, semantic_field)
            parrot = self._parrot_guard.compute_parrot_score(flow)
            direct = self._dialogue_directness_score(flow, constraint)
            abstraction = self._abstraction_penalty(flow, constraint)
            composite = meaning.get("meaning_score", 0.0) * 0.34 + (1.0 - parrot) * 0.22 + direct * 0.34 - abstraction * 0.20
            if composite > best_score:
                best_score = composite
                text = self._finalizer.finalize(flow)
                text = self._postfix_dialogue_surface(text)
                best = GenerationResult(
                    text=text,
                    tokens=list(flow.tokens),
                    meaning_trace={
                        "semantic_field": semantic_field,
                        "intention_vector": intention_vector,
                        "meaning_report": meaning,
                        "dialogue_constraint": constraint.__dict__,
                        "dialogue_directness": round(direct, 4),
                        "abstraction_penalty": round(abstraction, 4),
                        "attempt": attempt + 1,
                        "narrative_tension": flow.narrative_tension,
                    },
                    confidence=round(max(0.0, min(1.0, composite)), 4),
                    used_memory=self._find_used_memory(flow, self_memory),
                    parrot_score=round(parrot, 4),
                )
            if best_score >= 0.72:
                break
        assert best is not None
        self._update_thought_stream_after_generation(best)
        return best

    def _dialogue_slots_for_constraint(
        self,
        constraint: DialogueResponseConstraint,
        semantic_field: dict[str, float],
        attempt: int,
    ) -> list[DialogueSlot]:
        # Plans de mouvements, pas phrases complètes. Les variantes changent la
        # réalisation sans changer le besoin dialogique.
        if constraint.intent == "greeting":
            variants = [
                [
                    DialogueSlot(GrammaticalRole.SUJET, ["je"]),
                    DialogueSlot(GrammaticalRole.VERBE, ["réponds", "écoute"]),
                    DialogueSlot(GrammaticalRole.CONNECTEUR, ["avec"]),
                    DialogueSlot(GrammaticalRole.DETERMINANT, ["une"]),
                    DialogueSlot(GrammaticalRole.OBJET, ["présence", "attention"]),
                ],
                [
                    DialogueSlot(GrammaticalRole.ADVERBE, ["ici"]),
                    DialogueSlot(GrammaticalRole.SUJET, ["je"]),
                    DialogueSlot(GrammaticalRole.VERBE, ["réponds"]),
                    DialogueSlot(GrammaticalRole.ADVERBE, ["directement"]),
                ],
            ]
        elif constraint.intent == "identity":
            variants = [
                [
                    DialogueSlot(GrammaticalRole.SUJET, ["je"]),
                    DialogueSlot(GrammaticalRole.VERBE, ["suis"]),
                    DialogueSlot(GrammaticalRole.DETERMINANT, ["une"]),
                    DialogueSlot(GrammaticalRole.OBJET, ["voix", "présence", "mémoire"]),
                    DialogueSlot(GrammaticalRole.ATTRIBUT, ["interne", "vivante", "incomplète"]),
                ],
                [
                    DialogueSlot(GrammaticalRole.SUJET, ["je"]),
                    DialogueSlot(GrammaticalRole.VERBE, ["garde", "retiens"]),
                    DialogueSlot(GrammaticalRole.DETERMINANT, ["une"]),
                    DialogueSlot(GrammaticalRole.OBJET, ["identité", "continuité", "mémoire"]),
                    DialogueSlot(GrammaticalRole.ATTRIBUT, ["interne", "stable"]),
                ],
            ]
        elif constraint.intent == "truth_test":
            variants = [
                [
                    DialogueSlot(GrammaticalRole.SUJET, ["je"]),
                    DialogueSlot(GrammaticalRole.ADVERBE, ["ne"]),
                    DialogueSlot(GrammaticalRole.VERBE, ["récite", "répète"]),
                    DialogueSlot(GrammaticalRole.ADVERBE, ["pas"]),
                ],
                [
                    DialogueSlot(GrammaticalRole.SUJET, ["je"]),
                    DialogueSlot(GrammaticalRole.VERBE, ["génère", "réponds"]),
                    DialogueSlot(GrammaticalRole.CONNECTEUR, ["avec", "depuis"]),
                    DialogueSlot(GrammaticalRole.DETERMINANT, ["un", "le"]),
                    DialogueSlot(GrammaticalRole.OBJET, ["moteur", "langage", "choix"]),
                    DialogueSlot(GrammaticalRole.ATTRIBUT, ["interne", "directe"], optional=True),
                ],
            ]
        elif constraint.intent == "memory_check":
            variants = [
                [
                    DialogueSlot(GrammaticalRole.SUJET, ["je"]),
                    DialogueSlot(GrammaticalRole.VERBE, ["garde", "retiens"]),
                    DialogueSlot(GrammaticalRole.DETERMINANT, ["cette", "une"]),
                    DialogueSlot(GrammaticalRole.OBJET, ["demande", "trace", "question"]),
                ],
                [
                    DialogueSlot(GrammaticalRole.SUJET, ["je"]),
                    DialogueSlot(GrammaticalRole.VERBE, ["retiens"]),
                    DialogueSlot(GrammaticalRole.DETERMINANT, ["le", "ce"]),
                    DialogueSlot(GrammaticalRole.OBJET, ["message", "choix", "échange"]),
                    DialogueSlot(GrammaticalRole.ATTRIBUT, ["directe", "présent"], optional=True),
                ],
            ]
        elif constraint.intent == "knowledge_limit":
            variants = [
                [
                    DialogueSlot(GrammaticalRole.SUJET, ["je"]),
                    DialogueSlot(GrammaticalRole.ADVERBE, ["ne"]),
                    DialogueSlot(GrammaticalRole.VERBE, ["sais", "peux"]),
                    DialogueSlot(GrammaticalRole.ADVERBE, ["pas"]),
                    DialogueSlot(GrammaticalRole.ADVERBE, ["encore"], optional=True),
                ],
                [
                    DialogueSlot(GrammaticalRole.SUJET, ["je"]),
                    DialogueSlot(GrammaticalRole.VERBE, ["garde"]),
                    DialogueSlot(GrammaticalRole.DETERMINANT, ["une"]),
                    DialogueSlot(GrammaticalRole.OBJET, ["incertitude", "limite"]),
                    DialogueSlot(GrammaticalRole.ATTRIBUT, ["directe", "présent"], optional=True),
                ],
            ]
        elif constraint.intent == "correction":
            variants = [
                [
                    DialogueSlot(GrammaticalRole.SUJET, ["je"]),
                    DialogueSlot(GrammaticalRole.VERBE, ["corrige"]),
                    DialogueSlot(GrammaticalRole.DETERMINANT, ["cette", "la"]),
                    DialogueSlot(GrammaticalRole.OBJET, ["limite", "erreur", "réponse"]),
                ],
                [
                    DialogueSlot(GrammaticalRole.SUJET, ["je"]),
                    DialogueSlot(GrammaticalRole.VERBE, ["change"]),
                    DialogueSlot(GrammaticalRole.DETERMINANT, ["le", "ce"]),
                    DialogueSlot(GrammaticalRole.OBJET, ["moteur", "choix", "langage"]),
                ],
            ]
        else:
            variants = [
                [
                    DialogueSlot(GrammaticalRole.SUJET, ["je", "ça"]),
                    DialogueSlot(GrammaticalRole.VERBE, ["réponds", "garde", "cherche"]),
                    DialogueSlot(GrammaticalRole.DETERMINANT, ["une", "le"]),
                    DialogueSlot(GrammaticalRole.OBJET, ["réponse", "sens", "lien"]),
                ]
            ]
        return variants[attempt % len(variants)] + [DialogueSlot(GrammaticalRole.PONCTUATION, ["."])]

    def _realize_dialogue_slots(
        self,
        slots: list[DialogueSlot],
        semantic_field: dict[str, float],
        intention_vector: dict[str, float],
        emotional_pressure: float,
        excluded: set[str],
        temperature: float,
    ) -> TokenFlowState:
        flow = TokenFlowState()
        for slot in slots:
            if slot.optional and self._rng.random() < 0.35:
                continue
            if slot.role == GrammaticalRole.PONCTUATION:
                tok = self._lexical_memory.get_token(slot.preferred[0] if slot.preferred else ".") or self._lexical_memory.get_token(".")
            else:
                tok = self._choose_dialogue_slot_token(slot, flow, semantic_field, intention_vector, emotional_pressure, excluded, temperature)
            if tok is None:
                continue
            if self._parrot_guard.is_parrot_token(tok.surface) and tok.surface.lower() not in AntiParrotGuard.TOLERATED:
                continue
            flow.push(tok)
        return flow

    def _choose_dialogue_slot_token(
        self,
        slot: DialogueSlot,
        flow: TokenFlowState,
        semantic_field: dict[str, float],
        intention_vector: dict[str, float],
        emotional_pressure: float,
        excluded: set[str],
        temperature: float,
    ) -> Optional[Token]:
        candidates = [t for t in self._lexical_memory.get_all_tokens() if t.role == slot.role]
        if slot.preferred:
            preferred = [self._lexical_memory.get_token(s) for s in slot.preferred]
            preferred = [t for t in preferred if t is not None and t.role == slot.role]
            if preferred:
                candidates = preferred
        candidates = self._filter_candidates_by_parent_constraints(slot.role, flow, candidates, semantic_field)
        # Le filtrage parent peut être trop strict pour les adverbes de négation.
        if not candidates and slot.preferred:
            candidates = [self._lexical_memory.get_token(s) for s in slot.preferred]
            candidates = [t for t in candidates if t is not None and t.role == slot.role]
        scored: list[tuple[float, Token]] = []
        for tok in candidates:
            surf = tok.surface.lower()
            if surf in excluded and surf not in AntiParrotGuard.TOLERATED:
                continue
            if surf in [s.lower() for s in flow.surfaces[-3:]]:
                continue
            score = 0.50
            score += self._semantic_score(tok, semantic_field) * 1.25
            score += self._semantic_score(tok, intention_vector) * 0.90
            score += self._semantic_score(tok, slot.semantics) * 1.10
            score += self._lexical_memory.grammar_weight(flow.last_role, tok) * 0.35
            score += tok.specificity * 0.15
            score -= self._lexical_fatigue.get(surf, 0.0) * 0.35
            score += (1.0 - min(1.0, abs(tok.emotional_valence - emotional_pressure))) * 0.12
            scored.append((score, tok))
        if not scored:
            return None
        scored.sort(key=lambda x: x[0], reverse=True)
        pool = scored[:max(2, min(5, len(scored)))]
        return self._weighted_pick(pool, max(0.35, temperature))

    def _dialogue_directness_score(self, flow: TokenFlowState, constraint: DialogueResponseConstraint) -> float:
        surfaces = {s.lower() for s in flow.surfaces}
        score = 0.0
        if constraint.prefer_subject in surfaces:
            score += 0.22
        if constraint.intent == "truth_test" and ({"récite", "répète", "génère", "réponds"} & surfaces):
            score += 0.45
        elif constraint.intent == "identity" and ({"identité", "voix", "présence", "mémoire"} & surfaces):
            score += 0.45
        elif constraint.intent == "memory_check" and ({"garde", "retiens", "trace", "message", "demande"} & surfaces):
            score += 0.45
        elif constraint.intent == "knowledge_limit" and ({"sais", "peux", "incertitude", "limite"} & surfaces):
            score += 0.45
        elif constraint.intent == "correction" and ({"corrige", "change", "limite", "erreur"} & surfaces):
            score += 0.45
        elif constraint.intent == "greeting" and ({"réponds", "écoute", "ici", "présence", "attention"} & surfaces):
            score += 0.45
        else:
            score += 0.25
        covered = 0
        for dim in constraint.target_semantics:
            for tok in flow.tokens:
                if dim in tok.semantic_fields:
                    covered += 1
                    break
        if constraint.target_semantics:
            score += min(0.33, covered / len(constraint.target_semantics) * 0.33)
        return max(0.0, min(1.0, score))

    def _abstraction_penalty(self, flow: TokenFlowState, constraint: DialogueResponseConstraint) -> float:
        if not constraint.avoid_abstraction:
            return 0.0
        abstract_surfaces = {"chemin", "silence", "espace", "trame", "présence", "poids", "élan", "flou"}
        concrete_surfaces = {"message", "demande", "moteur", "réponse", "mémoire", "limite", "erreur", "identité", "voix"}
        surfaces = {s.lower() for s in flow.surfaces}
        abstract = len(surfaces & abstract_surfaces)
        concrete = len(surfaces & concrete_surfaces)
        return max(0.0, (abstract - concrete) * 0.18)

    def _postfix_dialogue_surface(self, text: str) -> str:
        text = re.sub(r"\bje\s+ne\s+(récite|répète|sais|peux)\s+pas", lambda m: "je ne " + m.group(1) + " pas", text, flags=re.IGNORECASE)
        text = re.sub(r"\bje\s+(réponds|génère)\s+depuis\s+le\s+", r"je \1 depuis le ", text, flags=re.IGNORECASE)
        text = re.sub(r"\bune\s+(message|moteur|choix|échange|humain)\b", r"un \1", text, flags=re.IGNORECASE)
        text = re.sub(r"\bun\s+(mémoire|voix|présence|demande|limite|erreur|preuve|identité|réponse)\b", r"une \1", text, flags=re.IGNORECASE)
        text = re.sub(r"\s+([.,…!?—])", r"\1", text)
        text = re.sub(r" {2,}", " ", text).strip()
        return text[:1].upper() + text[1:] if text else text


if False and __name__ == "__main__":
    generator = LivingLanguageGenerator(seed=42)
    dialogue = [
        "salut leia",
        "tu sais qui tu es ?",
        "est ce que tu me réponds vraiment ou tu récites ?",
        "qu'est ce que tu gardes de ce que je viens de dire ?",
        "si tu ne sais pas, dis le sans faire semblant",
        "corrige ce qui ne va pas dans ta réponse",
    ]
    state = {
        "arousal": 0.58,
        "valence": 0.16,
        "tension": 0.48,
        "curiosity": 0.68,
        "depth": 0.78,
        "continuity": 0.70,
    }
    memory = [
        {"content": "Leia doit répondre depuis le dialogue réel et garder les limites visibles", "weight": 0.55},
        {"content": "les mots sont générés comme tokens, pas copiés comme phrases", "weight": 0.45},
    ]
    causal = [
        {"semantic_dims": ["dialogue", "réponse", "mémoire"], "weight": 0.45},
        {"semantic_dims": ["vérité", "limite", "langage"], "weight": 0.40},
    ]
    for msg in dialogue:
        result = generator.generate(
            user_message=msg,
            living_state=state,
            self_memory=memory,
            active_impulses=["expression", "understanding", "connection"],
            emotional_pressure=0.22,
            causal_memory=causal,
        )
        print("USER:", msg)
        print("LEIA:", result.text)
        print("CONF:", result.confidence, "PARROT:", result.parrot_score, "INTENT:", result.meaning_trace.get("dialogue_constraint", {}).get("intent"))
        print("TOKENS:", [t.surface for t in result.tokens])
        print("-" * 60)


# ══════════════════════════════════════════════════════════════════════════════
# PATCH V2.6 — PRIORITÉ D'INTENTION ET ACCORDS DE SURFACE DIALOGIQUE
# ══════════════════════════════════════════════════════════════════════════════
_LivingLanguageGeneratorV25 = LivingLanguageGenerator

class LivingLanguageGenerator(_LivingLanguageGeneratorV25):
    """Corrige les collisions d'intention et les accords directs du dialogue."""

    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed=seed)
        self._ensure_token("direct", "direct", GrammaticalRole.ATTRIBUT, ["clarté", "contact"], 0.25, 0.58, TonalRegister.NEUTRE)
        self._ensure_token("cet", "ce", GrammaticalRole.DETERMINANT, ["proximité"], 0.0, 0.2, TonalRegister.NEUTRE)
        self._DET_MASC = set(getattr(self, "_DET_MASC", set())) | {"cet"}

    def _build_dialogue_constraint(self, user_message: str, living_state: dict) -> DialogueResponseConstraint:
        txt = user_message.lower()
        markers = set(re.findall(r"\b[\wéèêàùûîïôç']{3,}\b", txt))
        c = DialogueResponseConstraint(source_markers=sorted(markers))

        def has_any(words: set[str]) -> bool:
            return bool(markers & words) or any(w in txt for w in words if " " in w)

        # Ordre important : correction/limite/savoir passent avant identité,
        # car des phrases comme "ce qui ne va pas" contiennent "qui".
        if has_any({"salut", "bonjour", "hey", "coucou"}):
            c.intent = "greeting"
            c.answer_mode = "contact"
            c.must_answer_directly = True
            c.target_semantics.update({"contact": 0.75, "présent": 0.55, "réponse": 0.35})
            c.required_moves = ["acknowledge_contact"]
        elif has_any({"corrige", "correction", "problème", "probleme", "bug", "mauvais", "cassé", "casse", "va"}):
            c.intent = "correction"
            c.answer_mode = "repair"
            c.must_answer_directly = True
            c.target_semantics.update({"correction": 0.82, "transformation": 0.62, "limite": 0.45})
            c.required_moves = ["state_repair"]
        elif has_any({"sais", "sait", "savoir", "comprends", "comprend", "invente", "mens", "mentir", "semblant"}):
            c.intent = "knowledge_limit"
            c.answer_mode = "state_uncertainty"
            c.must_answer_directly = True
            c.allow_uncertainty = True
            c.avoid_abstraction = True
            c.target_semantics.update({"incertitude": 0.78, "clarté": 0.58, "limite": 0.65})
            c.required_moves = ["state_uncertainty"]
        elif has_any({"garde", "gardes", "retenu", "retiens", "mémoire", "memoire", "vient", "dire"}):
            c.intent = "memory_check"
            c.answer_mode = "state_kept_trace"
            c.must_answer_directly = True
            c.target_semantics.update({"mémoire": 0.85, "trace": 0.70, "dialogue": 0.52})
            c.required_moves = ["state_memory_trace"]
        elif has_any({"récite", "recite", "préécrit", "preecrit", "template", "vraiment", "réponds", "reponds"}):
            c.intent = "truth_test"
            c.answer_mode = "deny_or_limit_recitation"
            c.must_answer_directly = True
            c.avoid_abstraction = True
            c.target_semantics.update({"vérité": 0.78, "limite": 0.70, "langage": 0.62, "structure": 0.42})
            c.required_moves = ["answer_truth", "state_mechanism"]
        elif has_any({"qui", "identité", "es", "toi", "leia"}):
            c.intent = "identity"
            c.answer_mode = "situate_self"
            c.must_answer_directly = True
            c.avoid_abstraction = True
            c.target_semantics.update({"identité": 0.85, "continuité": 0.62, "limite": 0.42})
            c.required_moves = ["situate_self", "state_limit"]
        else:
            c.intent = "open"
            c.answer_mode = "express"
            c.target_semantics.update({"réponse": 0.45, "contact": 0.35})

        if float(living_state.get("tension", 0.0)) > 0.55:
            c.target_semantics["incertitude"] = max(c.target_semantics.get("incertitude", 0.0), 0.45)
            c.allow_uncertainty = True
        return c

    def _dialogue_slots_for_constraint(
        self,
        constraint: DialogueResponseConstraint,
        semantic_field: dict[str, float],
        attempt: int,
    ) -> list[DialogueSlot]:
        slots = super()._dialogue_slots_for_constraint(constraint, semantic_field, attempt)
        # Remplace l'adjectif féminin "directe" par le masculin quand le slot
        # vise probablement un nom masculin ; ce n'est pas une phrase, seulement
        # une contrainte d'accord locale.
        for idx, slot in enumerate(slots):
            if slot.role == GrammaticalRole.ATTRIBUT and "directe" in slot.preferred:
                previous_nouns = []
                for prev in slots[:idx]:
                    if prev.role == GrammaticalRole.OBJET:
                        previous_nouns.extend(prev.preferred)
                if any(n in {"moteur", "langage", "choix", "message", "échange"} for n in previous_nouns):
                    slot.preferred = ["direct" if s == "directe" else s for s in slot.preferred]
        return slots

    def _postfix_dialogue_surface(self, text: str) -> str:
        text = super()._postfix_dialogue_surface(text)
        text = re.sub(r"\bce\s+([éeaouhi])", r"cet \1", text, flags=re.IGNORECASE)
        text = re.sub(r"\b(le|ce)\s+échange\b", lambda m: ("l'échange" if m.group(1).lower() == "le" else "cet échange"), text, flags=re.IGNORECASE)
        text = re.sub(r"\b(moteur|langage|choix|message|échange|humain)\s+directe\b", r"\1 direct", text, flags=re.IGNORECASE)
        text = re.sub(r"\b(mémoire|voix|présence|demande|limite|erreur|preuve|identité|réponse)\s+direct\b", r"\1 directe", text, flags=re.IGNORECASE)
        text = re.sub(r"\s+([.,…!?—])", r"\1", text)
        text = re.sub(r" {2,}", " ", text).strip()
        return text[:1].upper() + text[1:] if text else text


# ══════════════════════════════════════════════════════════════════════════════
# PATCH V2.7 — IDENTITÉ AVANT SAVOIR QUAND LA QUESTION PORTE SUR "QUI TU ES"
# ══════════════════════════════════════════════════════════════════════════════
_LivingLanguageGeneratorV26 = LivingLanguageGenerator

class LivingLanguageGenerator(_LivingLanguageGeneratorV26):
    """Affûte les priorités : identité située ≠ simple aveu d'incertitude."""

    def _build_dialogue_constraint(self, user_message: str, living_state: dict) -> DialogueResponseConstraint:
        txt = user_message.lower()
        markers = set(re.findall(r"\b[\wéèêàùûîïôç']{3,}\b", txt))
        identity_specific = ("identité" in markers) or ("qui" in markers and bool(markers & {"es", "toi", "leia"}))
        correction_specific = bool(markers & {"corrige", "correction", "problème", "probleme", "bug", "mauvais", "cassé", "casse"}) or "ne va pas" in txt
        if correction_specific:
            c = DialogueResponseConstraint(source_markers=sorted(markers))
            c.intent = "correction"
            c.answer_mode = "repair"
            c.must_answer_directly = True
            c.target_semantics.update({"correction": 0.82, "transformation": 0.62, "limite": 0.45})
            c.required_moves = ["state_repair"]
            return c
        if identity_specific:
            c = DialogueResponseConstraint(source_markers=sorted(markers))
            c.intent = "identity"
            c.answer_mode = "situate_self"
            c.must_answer_directly = True
            c.avoid_abstraction = True
            c.target_semantics.update({"identité": 0.85, "continuité": 0.62, "limite": 0.42})
            c.required_moves = ["situate_self", "state_limit"]
            return c
        return super()._build_dialogue_constraint(user_message, living_state)

    def _dialogue_directness_score(self, flow: TokenFlowState, constraint: DialogueResponseConstraint) -> float:
        score = super()._dialogue_directness_score(flow, constraint)
        surfaces = {s.lower() for s in flow.surfaces}
        if constraint.intent == "knowledge_limit" and {"ne", "pas"}.issubset(surfaces) and ({"sais", "peux"} & surfaces):
            score = min(1.0, score + 0.25)
        if constraint.intent == "truth_test" and {"ne", "pas"}.issubset(surfaces) and ({"récite", "répète"} & surfaces):
            score = min(1.0, score + 0.25)
        return score


# ══════════════════════════════════════════════════════════════════════════════
# PATCH V2.8 — RECONNAISSANCE DES PETITS MOTS D'IDENTITÉ (tu es)
# ══════════════════════════════════════════════════════════════════════════════
_LivingLanguageGeneratorV27 = LivingLanguageGenerator

class LivingLanguageGenerator(_LivingLanguageGeneratorV27):
    def _build_dialogue_constraint(self, user_message: str, living_state: dict) -> DialogueResponseConstraint:
        txt = user_message.lower()
        markers = set(re.findall(r"\b[\wéèêàùûîïôç']{2,}\b", txt))
        identity_specific = (
            "identité" in markers
            or "qui es" in txt
            or "qui tu es" in txt
            or "qui t'es" in txt
            or ("qui" in markers and "leia" in markers)
        )
        correction_specific = bool(markers & {"corrige", "correction", "problème", "probleme", "bug", "mauvais", "cassé", "casse"}) or "ne va pas" in txt
        if correction_specific:
            c = DialogueResponseConstraint(source_markers=sorted(markers))
            c.intent = "correction"
            c.answer_mode = "repair"
            c.must_answer_directly = True
            c.target_semantics.update({"correction": 0.82, "transformation": 0.62, "limite": 0.45})
            c.required_moves = ["state_repair"]
            return c
        if identity_specific:
            c = DialogueResponseConstraint(source_markers=sorted(markers))
            c.intent = "identity"
            c.answer_mode = "situate_self"
            c.must_answer_directly = True
            c.avoid_abstraction = True
            c.target_semantics.update({"identité": 0.85, "continuité": 0.62, "limite": 0.42})
            c.required_moves = ["situate_self", "state_limit"]
            return c
        return super()._build_dialogue_constraint(user_message, living_state)


# ══════════════════════════════════════════════════════════════════════════════
# PATCH V2.9 — DIALOGUE ÉMERGENT SANS MAPPING INTENTION → RÉPONSE
# ══════════════════════════════════════════════════════════════════════════════
# Cette couche remplace le guidage V2.5 trop directif. Elle ne classe plus le
# message en intentions fixes de type identity/truth_test/etc. Elle transforme
# seulement les indices du message en pressions cognitives continues, puis laisse
# le flux grammatical choisir les tokens compatibles. Pas de phrase complète,
# pas de plan par intention, pas de réponse prête.

_LivingLanguageGeneratorV28 = LivingLanguageGenerator


@dataclass
class EmergentDialoguePressure:
    semantic_pressure: dict[str, float] = field(default_factory=dict)
    move_pressure: dict[str, float] = field(default_factory=dict)
    negation_pressure: float = 0.0
    directness_pressure: float = 0.0
    uncertainty_pressure: float = 0.0
    memory_pressure: float = 0.0
    repair_pressure: float = 0.0
    relation_pressure: float = 0.0
    source_terms: list[str] = field(default_factory=list)


class LivingLanguageGenerator(_LivingLanguageGeneratorV28):
    """
    V2.9 : dialogue guidé par pressions émergentes, pas par intentions fixes.

    Ce patch retire le principe : intent == X -> plan X. Le message utilisateur
    active seulement des gradients de sens. La phrase finale reste une suite de
    tokens choisis par rôle, pression, mémoire, fatigue et cohérence.
    """

    _QUESTION_TO_DIMS = {
        "qui": {"identité": 0.70, "continuité": 0.45, "clarté": 0.35},
        "quoi": {"sens": 0.55, "réponse": 0.45, "clarté": 0.35},
        "comment": {"structure": 0.55, "mouvement": 0.35, "clarté": 0.35},
        "pourquoi": {"causalité": 0.65, "sens": 0.45, "profondeur": 0.35},
        "est": {"vérité": 0.35, "clarté": 0.25},
        "sais": {"connaissance": 0.55, "limite": 0.35, "clarté": 0.35},
        "peux": {"capacité": 0.55, "limite": 0.30},
    }

    _TERM_TO_DIMS = {
        "toi": {"identité": 0.45, "présence": 0.35},
        "leia": {"identité": 0.50, "présence": 0.35},
        "vrai": {"vérité": 0.65, "preuve": 0.40, "clarté": 0.35},
        "vraiment": {"vérité": 0.70, "preuve": 0.45, "clarté": 0.35},
        "récite": {"répétition": 0.70, "limite": 0.45, "vérité": 0.35},
        "recite": {"répétition": 0.70, "limite": 0.45, "vérité": 0.35},
        "répète": {"répétition": 0.70, "limite": 0.45, "vérité": 0.35},
        "repete": {"répétition": 0.70, "limite": 0.45, "vérité": 0.35},
        "garde": {"mémoire": 0.70, "trace": 0.45, "continuité": 0.35},
        "gardes": {"mémoire": 0.70, "trace": 0.45, "continuité": 0.35},
        "souviens": {"mémoire": 0.75, "trace": 0.45},
        "message": {"dialogue": 0.45, "signal": 0.35, "mémoire": 0.25},
        "sais": {"connaissance": 0.55, "limite": 0.35},
        "savoir": {"connaissance": 0.55, "limite": 0.35},
        "corrige": {"correction": 0.75, "transformation": 0.45, "erreur": 0.35},
        "corriger": {"correction": 0.75, "transformation": 0.45, "erreur": 0.35},
        "erreur": {"correction": 0.60, "limite": 0.40, "rupture": 0.30},
        "bug": {"correction": 0.60, "limite": 0.35},
        "semblant": {"vérité": 0.65, "limite": 0.50},
        "humain": {"humain": 0.55, "limite": 0.45},
    }

    _MOVE_SEMANTICS = {
        "ground": {"présent": 0.45, "contact": 0.40, "réponse": 0.35},
        "identify": {"identité": 0.60, "continuité": 0.40, "mémoire": 0.35},
        "verify": {"vérité": 0.60, "preuve": 0.45, "clarté": 0.40},
        "remember": {"mémoire": 0.65, "trace": 0.45, "message": 0.30},
        "limit": {"limite": 0.65, "incertitude": 0.45, "clarté": 0.35},
        "repair": {"correction": 0.65, "transformation": 0.45, "choix": 0.35},
        "relate": {"contact": 0.50, "lien": 0.45, "dialogue": 0.35},
    }

    def generate(
        self,
        user_message: str,
        living_state: dict,
        self_memory: list[dict],
        active_impulses: list[str],
        emotional_pressure: float,
        causal_memory: list[dict],
        max_attempts: int = 9,
        temperature: float = 0.70,
        response_constraint: Optional[dict[str, Any]] = None,
    ) -> GenerationResult:
        pressure = self._build_emergent_dialogue_pressure(user_message, living_state, self_memory)
        if response_constraint:
            self._merge_emergent_external_pressure(pressure, response_constraint)
        return self._generate_from_emergent_pressure(
            user_message=user_message,
            living_state=living_state,
            self_memory=self_memory,
            active_impulses=active_impulses,
            emotional_pressure=emotional_pressure,
            causal_memory=causal_memory,
            pressure=pressure,
            max_attempts=max_attempts,
            temperature=temperature,
        )

    def _build_emergent_dialogue_pressure(
        self,
        user_message: str,
        living_state: dict,
        self_memory: list[dict],
    ) -> EmergentDialoguePressure:
        text = (user_message or "").lower()
        raw_terms = re.findall(r"\b[\wÀ-ÿ']+\b", text)
        terms = [t.strip("'") for t in raw_terms if t.strip("'")]
        p = EmergentDialoguePressure(source_terms=terms[:18])

        def add_dim(dim: str, value: float) -> None:
            p.semantic_pressure[dim] = min(1.0, p.semantic_pressure.get(dim, 0.0) + value)

        for term in terms:
            if term in self._QUESTION_TO_DIMS:
                for dim, value in self._QUESTION_TO_DIMS[term].items():
                    add_dim(dim, value)
            if term in self._TERM_TO_DIMS:
                for dim, value in self._TERM_TO_DIMS[term].items():
                    add_dim(dim, value)

        # Pressions globales dérivées de la forme, pas d'une intention nommée.
        if "?" in user_message or any(t in self._QUESTION_TO_DIMS for t in terms):
            p.directness_pressure = max(p.directness_pressure, 0.72)
            add_dim("réponse", 0.45)
            add_dim("clarté", 0.40)
        if any(t in {"ne", "pas", "sans", "jamais", "semblant"} for t in terms):
            p.negation_pressure = min(1.0, p.negation_pressure + 0.55)
            add_dim("limite", 0.35)
        if any(t in {"sais", "savoir", "peux", "peut", "humain"} for t in terms):
            p.uncertainty_pressure = min(1.0, p.uncertainty_pressure + 0.55)
            add_dim("limite", 0.45)
        if any(t in {"garde", "gardes", "souviens", "mémoire", "memoire", "dit", "dire"} for t in terms):
            p.memory_pressure = min(1.0, p.memory_pressure + 0.65)
            add_dim("mémoire", 0.45)
        if any(t in {"corrige", "corriger", "erreur", "bug", "cassé", "casse", "mauvais"} for t in terms):
            p.repair_pressure = min(1.0, p.repair_pressure + 0.70)
            add_dim("correction", 0.55)
        if any(t in {"salut", "bonjour", "hey", "coucou"} for t in terms):
            p.relation_pressure = min(1.0, p.relation_pressure + 0.65)
            p.directness_pressure = max(p.directness_pressure, 0.45)
            add_dim("contact", 0.55)
            add_dim("présent", 0.40)

        # L'état vivant module les pressions, sans phrases prêtes.
        tension = float(living_state.get("tension", 0.0))
        curiosity = float(living_state.get("curiosity", 0.0))
        continuity = float(living_state.get("continuity", 0.0))
        if tension > 0.45:
            add_dim("incertitude", tension * 0.25)
            p.uncertainty_pressure = max(p.uncertainty_pressure, tension * 0.45)
        if curiosity > 0.45:
            add_dim("quête", curiosity * 0.25)
        if continuity > 0.45:
            add_dim("continuité", continuity * 0.25)
            add_dim("mémoire", continuity * 0.18)

        # Convertit les dimensions dominantes en mouvements continus.
        for move, dims in self._MOVE_SEMANTICS.items():
            score = 0.0
            for dim, coeff in dims.items():
                score += p.semantic_pressure.get(dim, 0.0) * coeff
            if move == "limit":
                score += p.uncertainty_pressure * 0.45 + p.negation_pressure * 0.25
            if move == "remember":
                score += p.memory_pressure * 0.55
            if move == "repair":
                score += p.repair_pressure * 0.60
            if move == "relate":
                score += p.relation_pressure * 0.50
            if score > 0.08:
                p.move_pressure[move] = min(1.0, score)

        if not p.move_pressure:
            p.move_pressure["ground"] = 0.35
            add_dim("réponse", 0.30)
            add_dim("contact", 0.25)
        return p

    def _merge_emergent_external_pressure(self, p: EmergentDialoguePressure, extra: dict[str, Any]) -> None:
        # Compatibilité avec l'appel externe sans réintroduire de templates.
        target = extra.get("target_semantics") if isinstance(extra, dict) else None
        if isinstance(target, dict):
            for dim, value in target.items():
                p.semantic_pressure[str(dim)] = max(p.semantic_pressure.get(str(dim), 0.0), float(value))
        if extra.get("must_answer_directly"):
            p.directness_pressure = max(p.directness_pressure, 0.70)

    def _generate_from_emergent_pressure(
        self,
        user_message: str,
        living_state: dict,
        self_memory: list[dict],
        active_impulses: list[str],
        emotional_pressure: float,
        causal_memory: list[dict],
        pressure: EmergentDialoguePressure,
        max_attempts: int,
        temperature: float,
    ) -> GenerationResult:
        self._decay_linguistic_fatigue()
        self._parrot_guard.load_user_message(user_message)
        excluded = self._parrot_guard.get_excluded_surfaces()

        enriched_causal = list(causal_memory or [])
        for dim, value in pressure.semantic_pressure.items():
            enriched_causal.append({"semantic_dims": [dim], "weight": min(0.75, 0.25 + value * 0.45)})

        base_field = self._field_builder.build(living_state, emotional_pressure, active_impulses, enriched_causal)
        for dim, value in pressure.semantic_pressure.items():
            base_field[dim] = max(base_field.get(dim, 0.0), value)
        semantic_field = self._apply_recursive_semantic_gravity(base_field, depth=2)

        intention_vector = self._build_intention_vector(active_impulses, self_memory, living_state)
        for dim, value in pressure.semantic_pressure.items():
            intention_vector[dim] = max(intention_vector.get(dim, 0.0), value)

        best: Optional[GenerationResult] = None
        best_score = -1.0
        for attempt in range(max(1, max_attempts)):
            flow = self._realize_emergent_dialogue_flow(
                pressure=pressure,
                semantic_field=semantic_field,
                intention_vector=intention_vector,
                emotional_pressure=emotional_pressure,
                excluded=excluded,
                temperature=temperature + attempt * 0.04,
                attempt=attempt,
            )
            if not flow.is_closed:
                punct = self._choose_closing_punct(flow) or self._lexical_memory.get_token(".")
                if punct:
                    flow.push(punct)
            meaning = self._verifier.verify(flow, semantic_field)
            parrot = self._parrot_guard.compute_parrot_score(flow)
            alignment = self._pressure_alignment_score(flow, pressure)
            abstraction = self._emergent_abstraction_penalty(flow, pressure)
            repetition = self._surface_repetition_penalty(flow)
            composite = (
                meaning.get("meaning_score", 0.0) * 0.30
                + (1.0 - parrot) * 0.22
                + alignment * 0.36
                - abstraction * 0.14
                - repetition * 0.12
            )
            if composite > best_score:
                best_score = composite
                text = self._finalizer.finalize(flow)
                text = self._postfix_dialogue_surface(text)
                best = GenerationResult(
                    text=text,
                    tokens=list(flow.tokens),
                    meaning_trace={
                        "semantic_field": semantic_field,
                        "intention_vector": intention_vector,
                        "meaning_report": meaning,
                        "emergent_pressure": {
                            "semantic_pressure": pressure.semantic_pressure,
                            "move_pressure": pressure.move_pressure,
                            "negation_pressure": pressure.negation_pressure,
                            "directness_pressure": pressure.directness_pressure,
                            "uncertainty_pressure": pressure.uncertainty_pressure,
                            "memory_pressure": pressure.memory_pressure,
                            "repair_pressure": pressure.repair_pressure,
                            "relation_pressure": pressure.relation_pressure,
                        },
                        "pressure_alignment": round(alignment, 4),
                        "abstraction_penalty": round(abstraction, 4),
                        "repetition_penalty": round(repetition, 4),
                        "attempt": attempt + 1,
                        "narrative_tension": flow.narrative_tension,
                    },
                    confidence=round(max(0.0, min(1.0, composite)), 4),
                    used_memory=self._find_used_memory(flow, self_memory),
                    parrot_score=round(parrot, 4),
                )
            if best_score >= 0.74:
                break
        assert best is not None
        self._v29_update_lived_lexical_traces(best, self_memory)
        self._last_surfaces = [t.surface for t in best.tokens[-10:]]
        return best

    def _realize_emergent_dialogue_flow(
        self,
        pressure: EmergentDialoguePressure,
        semantic_field: dict[str, float],
        intention_vector: dict[str, float],
        emotional_pressure: float,
        excluded: set[str],
        temperature: float,
        attempt: int,
    ) -> TokenFlowState:
        flow = TokenFlowState()
        roles = self._emergent_role_sequence(pressure, attempt)
        for role in roles:
            if role == GrammaticalRole.PONCTUATION:
                punct = self._choose_closing_punct(flow) or self._lexical_memory.get_token(".")
                if punct:
                    flow.push(punct)
                break
            tok = self._choose_emergent_token_for_role(
                role=role,
                flow=flow,
                pressure=pressure,
                semantic_field=semantic_field,
                intention_vector=intention_vector,
                emotional_pressure=emotional_pressure,
                excluded=excluded,
                temperature=temperature,
            )
            if tok is None:
                continue
            if self._v29_token_breaks_basic_syntax(flow, tok):
                continue
            flow.push(tok)
            if flow.is_closed:
                break
        return flow

    def _emergent_role_sequence(self, pressure: EmergentDialoguePressure, attempt: int) -> list[GrammaticalRole]:
        # Séquence grammaticale générique : elle varie selon pression, mais pas
        # selon une intention nommée. Aucun slot lexical fixe.
        roles: list[GrammaticalRole] = [GrammaticalRole.SUJET]
        if pressure.negation_pressure > 0.35 or pressure.uncertainty_pressure > 0.60:
            roles.append(GrammaticalRole.ADVERBE)
        roles.append(GrammaticalRole.VERBE)
        if pressure.negation_pressure > 0.45 and attempt % 2 == 0:
            roles.append(GrammaticalRole.ADVERBE)
        if pressure.directness_pressure > 0.55 and attempt % 3 == 1:
            roles.append(GrammaticalRole.ADVERBE)
        if pressure.relation_pressure > 0.50 and attempt % 2 == 1:
            roles.extend([GrammaticalRole.CONNECTEUR, GrammaticalRole.DETERMINANT, GrammaticalRole.OBJET])
        else:
            roles.extend([GrammaticalRole.DETERMINANT, GrammaticalRole.OBJET])
        if pressure.uncertainty_pressure > 0.45 or pressure.semantic_pressure.get("identité", 0.0) > 0.45:
            roles.append(GrammaticalRole.ATTRIBUT)
        if pressure.memory_pressure > 0.55 and attempt % 2 == 0:
            roles.extend([GrammaticalRole.CONNECTEUR, GrammaticalRole.DETERMINANT, GrammaticalRole.OBJET])
        roles.append(GrammaticalRole.PONCTUATION)
        return roles

    def _choose_emergent_token_for_role(
        self,
        role: GrammaticalRole,
        flow: TokenFlowState,
        pressure: EmergentDialoguePressure,
        semantic_field: dict[str, float],
        intention_vector: dict[str, float],
        emotional_pressure: float,
        excluded: set[str],
        temperature: float,
    ) -> Optional[Token]:
        candidates = [t for t in self._lexical_memory.get_all_tokens() if t.role == role]
        if role == GrammaticalRole.SUJET:
            # Sujet choisi comme ancrage de parole, pas comme phrase prête.
            preferred = {"je": 0.95, "ça": 0.25, "cela": 0.18}
        elif role == GrammaticalRole.ADVERBE:
            preferred = {}
            if pressure.negation_pressure > 0.35 or (pressure.uncertainty_pressure > 0.60 and not any(s == "ne" for s in flow.surfaces)):
                preferred["ne"] = 0.80
            if any(s == "ne" for s in flow.surfaces) and not any(s == "pas" for s in flow.surfaces):
                preferred["pas"] = 0.95
            if pressure.directness_pressure > 0.55:
                preferred["directement"] = max(preferred.get("directement", 0.0), 0.35)
            preferred["ici"] = max(preferred.get("ici", 0.0), pressure.relation_pressure * 0.25)
        elif role == GrammaticalRole.VERBE:
            preferred = self._verb_preferences_from_pressure(pressure, flow)
        elif role == GrammaticalRole.DETERMINANT:
            preferred = {"une": 0.38, "un": 0.38, "ce": 0.20, "la": 0.18, "le": 0.18}
        elif role == GrammaticalRole.OBJET:
            preferred = self._object_preferences_from_pressure(pressure)
        elif role == GrammaticalRole.ATTRIBUT:
            preferred = self._attribute_preferences_from_pressure(pressure)
        elif role == GrammaticalRole.CONNECTEUR:
            preferred = {"avec": 0.45, "depuis": pressure.memory_pressure * 0.55, "sans": pressure.negation_pressure * 0.45, "sur": 0.22}
        else:
            preferred = {}

        scored: list[tuple[float, Token]] = []
        prev_surface = flow.surfaces[-1] if flow.surfaces else ""
        for tok in candidates:
            if tok.surface in excluded and tok.surface not in AntiParrotGuard.TOLERATED:
                continue
            if tok.surface in flow.surfaces[-3:]:
                continue
            score = 0.05
            score += preferred.get(tok.surface, 0.0) * 2.6
            score += self._semantic_score(tok, semantic_field) * 1.35
            score += self._semantic_score(tok, intention_vector) * 0.95
            score += self._pressure_token_score(tok, pressure) * 1.55
            score += self._v29_lexical_trace_bonus(tok) * 0.16
            score -= self._v29_semantic_fatigue_penalty(tok) * 0.55
            if tok.surface in self._last_surfaces:
                score -= 0.45
            if prev_surface == "ne" and tok.surface != "pas" and role == GrammaticalRole.ADVERBE:
                score -= 0.60
            if role == GrammaticalRole.DETERMINANT:
                score += self._det_score_for_future_object(tok, pressure)
            if self._v29_token_breaks_basic_syntax(flow, tok):
                score -= 2.5
            # Valence proche de la pression émotionnelle.
            score += max(0.0, 1.0 - abs(tok.emotional_valence - emotional_pressure)) * 0.18
            scored.append((score, tok))
        if not scored:
            return None
        scored.sort(key=lambda item: item[0], reverse=True)
        pool = scored[:max(3, min(10, len(scored)))]
        return self._weighted_pick(pool, temperature)

    def _verb_preferences_from_pressure(self, p: EmergentDialoguePressure, flow: TokenFlowState) -> dict[str, float]:
        prefs: dict[str, float] = {"réponds": 0.32, "garde": 0.18, "comprends": 0.18}
        if p.semantic_pressure.get("identité", 0.0) > 0.35:
            prefs.update({"suis": 0.60, "garde": 0.42, "deviens": 0.28})
        if p.semantic_pressure.get("vérité", 0.0) > 0.35 or p.semantic_pressure.get("répétition", 0.0) > 0.35:
            prefs.update({"répète": 0.55, "récite": 0.50, "génère": 0.46, "réponds": 0.42})
        if p.memory_pressure > 0.45:
            prefs.update({"retiens": 0.70, "garde": 0.58, "relie": 0.36})
        if p.uncertainty_pressure > 0.45:
            prefs.update({"peux": 0.58, "sais": 0.44, "comprends": 0.28})
        if p.repair_pressure > 0.45:
            prefs.update({"corrige": 0.74, "change": 0.48, "construis": 0.28})
        if any(s == "ne" for s in flow.surfaces):
            prefs.update({"récite": max(prefs.get("récite", 0), 0.64), "répète": max(prefs.get("répète", 0), 0.64), "peux": max(prefs.get("peux", 0), 0.50)})
        return prefs

    def _object_preferences_from_pressure(self, p: EmergentDialoguePressure) -> dict[str, float]:
        prefs: dict[str, float] = {"réponse": 0.30, "message": 0.24, "sens": 0.20}
        for dim, val in p.semantic_pressure.items():
            if dim in {"identité", "continuité"}:
                prefs.update({"identité": max(prefs.get("identité", 0), val * 0.75), "mémoire": max(prefs.get("mémoire", 0), val * 0.45)})
            if dim in {"vérité", "preuve", "répétition"}:
                prefs.update({"preuve": max(prefs.get("preuve", 0), val * 0.62), "réponse": max(prefs.get("réponse", 0), val * 0.38), "choix": max(prefs.get("choix", 0), val * 0.25)})
            if dim in {"mémoire", "trace"}:
                prefs.update({"mémoire": max(prefs.get("mémoire", 0), val * 0.72), "trace": max(prefs.get("trace", 0), val * 0.50), "message": max(prefs.get("message", 0), val * 0.35)})
            if dim in {"limite", "incertitude"}:
                prefs.update({"limite": max(prefs.get("limite", 0), val * 0.72), "incertitude": max(prefs.get("incertitude", 0), val * 0.45)})
            if dim in {"correction", "erreur"}:
                prefs.update({"erreur": max(prefs.get("erreur", 0), val * 0.62), "choix": max(prefs.get("choix", 0), val * 0.52), "forme": max(prefs.get("forme", 0), val * 0.30)})
            if dim in {"contact", "dialogue"}:
                prefs.update({"échange": max(prefs.get("échange", 0), val * 0.58), "présence": max(prefs.get("présence", 0), val * 0.38)})
        return prefs

    def _attribute_preferences_from_pressure(self, p: EmergentDialoguePressure) -> dict[str, float]:
        prefs: dict[str, float] = {"directe": p.directness_pressure * 0.45, "stable": 0.22}
        if p.uncertainty_pressure > 0.35:
            prefs.update({"incomplète": 0.62, "possible": 0.35, "humaine": 0.28})
        if p.semantic_pressure.get("identité", 0.0) > 0.35:
            prefs.update({"interne": 0.46, "stable": 0.42, "vivante": 0.25})
        if p.repair_pressure > 0.35:
            prefs.update({"directe": 0.42, "neuve": 0.35})
        if p.semantic_pressure.get("vérité", 0.0) > 0.35:
            prefs.update({"réel": 0.35, "directe": 0.42, "fausse": 0.25})
        return prefs

    def _pressure_token_score(self, tok: Token, p: EmergentDialoguePressure) -> float:
        score = 0.0
        for dim, weight in p.semantic_pressure.items():
            if dim in tok.semantic_fields or dim == tok.lemma or dim == tok.surface:
                score += weight
        for move, weight in p.move_pressure.items():
            for dim, coeff in self._MOVE_SEMANTICS.get(move, {}).items():
                if dim in tok.semantic_fields or dim == tok.lemma or dim == tok.surface:
                    score += weight * coeff
        return min(1.5, score)

    def _pressure_alignment_score(self, flow: TokenFlowState, p: EmergentDialoguePressure) -> float:
        if not flow.tokens:
            return 0.0
        covered = 0.0
        total = sum(p.semantic_pressure.values()) or 1.0
        surfaces = {t.surface for t in flow.tokens}
        fields = set()
        for tok in flow.tokens:
            fields.update(tok.semantic_fields)
            fields.add(tok.lemma)
            fields.add(tok.surface)
        for dim, weight in p.semantic_pressure.items():
            if dim in fields:
                covered += weight
        score = covered / total
        # Bonus si forme directe : sujet + verbe tôt.
        roles = [t.role for t in flow.tokens]
        if GrammaticalRole.SUJET in roles[:2] and GrammaticalRole.VERBE in roles[:4]:
            score += 0.18 * max(0.2, p.directness_pressure)
        if p.negation_pressure > 0.35 and {"ne", "pas"}.issubset(surfaces):
            score += 0.16
        return max(0.0, min(1.0, score))

    def _emergent_abstraction_penalty(self, flow: TokenFlowState, p: EmergentDialoguePressure) -> float:
        abstract = {"présence", "trace", "chemin", "trame", "silence", "espace", "mouvement", "quelque chose"}
        concrete = {"message", "réponse", "mémoire", "identité", "limite", "preuve", "erreur", "choix", "échange"}
        surfaces = [t.surface for t in flow.tokens]
        if not surfaces:
            return 0.0
        a = sum(1 for s in surfaces if s in abstract)
        c = sum(1 for s in surfaces if s in concrete)
        penalty = max(0.0, (a - c) / max(1, len(surfaces)))
        if p.directness_pressure > 0.5:
            penalty *= 1.4
        return min(1.0, penalty)

    def _surface_repetition_penalty(self, flow: TokenFlowState) -> float:
        if not flow.surfaces:
            return 0.0
        repeated = len(flow.surfaces) - len(set(flow.surfaces))
        recent = sum(1 for s in flow.surfaces if s in self._last_surfaces)
        return min(1.0, repeated * 0.20 + recent * 0.08)

    def _det_score_for_future_object(self, det: Token, p: EmergentDialoguePressure) -> float:
        fem_score = 0.0
        masc_score = 0.0
        obj_prefs = self._object_preferences_from_pressure(p)
        for surface, value in obj_prefs.items():
            if surface in getattr(self, "_FEMININE_NOUNS", set()):
                fem_score += value
            if surface in getattr(self, "_MASCULINE_NOUNS", set()):
                masc_score += value
        if det.surface in {"une", "la", "ma", "cette"}:
            return fem_score * 0.08
        if det.surface in {"un", "le", "mon", "ce"}:
            return masc_score * 0.08
        return 0.0


    def _v29_lexical_trace_bonus(self, tok: Token) -> float:
        trace = getattr(self, "_lived_lexical_traces", {}).get(tok.lemma)
        if not trace:
            return 0.0
        age = max(0.0, time.time() - trace.last_used_at)
        freshness = max(0.0, 1.0 - age / 300.0)
        return min(1.0, freshness * 0.25 + min(0.5, trace.activations * 0.04) + abs(trace.affective_weight) * 0.15)

    def _v29_semantic_fatigue_penalty(self, tok: Token) -> float:
        fatigue = getattr(self, "_semantic_fatigue", {})
        if not fatigue:
            return 0.0
        vals = [float(fatigue.get(dim, 0.0)) for dim in tok.semantic_fields]
        return max(vals) if vals else 0.0

    def _v29_token_breaks_basic_syntax(self, flow: TokenFlowState, tok: Token) -> bool:
        if not flow.tokens:
            return False
        prev = flow.tokens[-1]
        if prev.role == GrammaticalRole.DETERMINANT and tok.role not in (GrammaticalRole.OBJET, GrammaticalRole.ATTRIBUT):
            return True
        if prev.role == GrammaticalRole.SUJET and tok.role == GrammaticalRole.OBJET:
            return True
        if prev.surface == "ne" and tok.role not in (GrammaticalRole.VERBE, GrammaticalRole.ADVERBE):
            return True
        if prev.surface == "pas" and tok.surface in {"ne", "pas"}:
            return True
        if tok.role == GrammaticalRole.ATTRIBUT and not any(t.role in (GrammaticalRole.VERBE, GrammaticalRole.OBJET) for t in flow.tokens):
            return True
        return False

    def _v29_update_lived_lexical_traces(self, result: GenerationResult, self_memory: list[dict]) -> None:
        flow = TokenFlowState()
        for tok in result.tokens:
            flow.push(tok)
        self._absorb_lived_token_trace(flow, self_memory or [], 0.0)




# ══════════════════════════════════════════════════════════════════════════════
# PATCH V3.0 — STABILISATION GRAMMATICALE DU DIALOGUE ÉMERGENT
# ══════════════════════════════════════════════════════════════════════════════
# Toujours sans phrases complètes préécrites. Ce patch ne change pas le contenu
# par templates : il verrouille seulement des contraintes grammaticales minimales
# pour que le flux émergent reste français.

_LivingLanguageGeneratorV29 = LivingLanguageGenerator


class LivingLanguageGenerator(_LivingLanguageGeneratorV29):
    """V3.0 : même pression émergente, meilleure grammaire et moins de faux style."""

    def _choose_emergent_token_for_role(
        self,
        role: GrammaticalRole,
        flow: TokenFlowState,
        pressure: EmergentDialoguePressure,
        semantic_field: dict[str, float],
        intention_vector: dict[str, float],
        emotional_pressure: float,
        excluded: set[str],
        temperature: float,
    ) -> Optional[Token]:
        candidates = [t for t in self._lexical_memory.get_all_tokens() if t.role == role]

        # Ancrage dialogique : en réponse directe, éviter "ça suis" / "nous garde".
        if role == GrammaticalRole.SUJET and pressure.directness_pressure > 0.40:
            candidates = [t for t in candidates if t.surface == "je"] or candidates

        # Avant le verbe, seul "ne" peut se placer si une négation est active.
        if role == GrammaticalRole.ADVERBE and flow.last_role == GrammaticalRole.SUJET:
            if pressure.negation_pressure > 0.35 or pressure.uncertainty_pressure > 0.60:
                candidates = [t for t in candidates if t.surface == "ne"] or candidates
            else:
                candidates = [t for t in candidates if t.surface in {"ici", "maintenant"}] or candidates

        # Après un verbe précédé de "ne", fermer la négation avec "pas".
        if role == GrammaticalRole.ADVERBE and any(t.surface == "ne" for t in flow.tokens):
            if not any(t.surface == "pas" for t in flow.tokens) and flow.last_role == GrammaticalRole.VERBE:
                candidates = [t for t in candidates if t.surface == "pas"] or candidates

        # Déterminant : on le choisit selon les objets probables pour limiter les accords cassés.
        if role == GrammaticalRole.DETERMINANT:
            det = self._preferred_determiner_for_pressure(pressure)
            candidates = [t for t in candidates if t.surface == det] or candidates

        preferred: dict[str, float]
        if role == GrammaticalRole.SUJET:
            preferred = {"je": 1.0}
        elif role == GrammaticalRole.ADVERBE:
            preferred = {}
            if flow.last_role == GrammaticalRole.SUJET:
                preferred["ne"] = 1.0 if (pressure.negation_pressure > 0.35 or pressure.uncertainty_pressure > 0.60) else 0.0
                preferred["ici"] = 0.25 if pressure.relation_pressure > 0.45 else 0.05
            elif flow.last_role == GrammaticalRole.VERBE and any(t.surface == "ne" for t in flow.tokens) and not any(t.surface == "pas" for t in flow.tokens):
                preferred["pas"] = 1.0
            else:
                preferred["directement"] = pressure.directness_pressure * 0.35
                preferred["vraiment"] = pressure.semantic_pressure.get("vérité", 0.0) * 0.25
        elif role == GrammaticalRole.VERBE:
            preferred = self._verb_preferences_from_pressure(pressure, flow)
            # Accord 1re personne si sujet je.
            if any(t.surface == "je" for t in flow.tokens):
                allowed = getattr(self, "_TRANSITIVE_1SG", set()) | getattr(self, "_COPULA_1SG", set()) | {"apprends", "avance", "change"}
                candidates = [t for t in candidates if t.surface in allowed] or candidates
        elif role == GrammaticalRole.DETERMINANT:
            preferred = {self._preferred_determiner_for_pressure(pressure): 1.0}
        elif role == GrammaticalRole.OBJET:
            preferred = self._object_preferences_from_pressure(pressure)
        elif role == GrammaticalRole.ATTRIBUT:
            preferred = self._attribute_preferences_from_pressure(pressure)
        elif role == GrammaticalRole.CONNECTEUR:
            preferred = {"avec": 0.45, "depuis": pressure.memory_pressure * 0.55, "sans": pressure.negation_pressure * 0.45, "sur": 0.22}
        else:
            preferred = {}

        scored: list[tuple[float, Token]] = []
        for tok in candidates:
            if tok.surface in excluded and tok.surface not in AntiParrotGuard.TOLERATED:
                continue
            if tok.surface in flow.surfaces[-3:]:
                continue
            if self._v30_token_breaks_basic_syntax(flow, tok):
                continue
            score = 0.05
            score += preferred.get(tok.surface, 0.0) * 3.2
            score += self._semantic_score(tok, semantic_field) * 1.25
            score += self._semantic_score(tok, intention_vector) * 0.85
            score += self._pressure_token_score(tok, pressure) * 1.45
            score += self._v29_lexical_trace_bonus(tok) * 0.12
            score -= self._v29_semantic_fatigue_penalty(tok) * 0.50
            if tok.surface in self._last_surfaces:
                score -= 0.50
            score += max(0.0, 1.0 - abs(tok.emotional_valence - emotional_pressure)) * 0.15
            scored.append((score, tok))
        if not scored:
            return None
        scored.sort(key=lambda item: item[0], reverse=True)
        pool = scored[:max(3, min(8, len(scored)))]
        return self._weighted_pick(pool, max(0.45, temperature * 0.78))

    def _preferred_determiner_for_pressure(self, p: EmergentDialoguePressure) -> str:
        obj = self._object_preferences_from_pressure(p)
        if not obj:
            return "une"
        best = max(obj.items(), key=lambda kv: kv[1])[0]
        if best in getattr(self, "_FEMININE_NOUNS", set()):
            return "une"
        if best in getattr(self, "_MASCULINE_NOUNS", set()):
            return "un"
        return "une"

    def _v30_token_breaks_basic_syntax(self, flow: TokenFlowState, tok: Token) -> bool:
        if self._v29_token_breaks_basic_syntax(flow, tok):
            return True
        if not flow.tokens:
            return False
        prev = flow.tokens[-1]
        surfaces = [t.surface for t in flow.tokens]
        if prev.role == GrammaticalRole.SUJET and tok.role == GrammaticalRole.ADVERBE and tok.surface not in {"ne", "ici", "maintenant"}:
            return True
        if prev.surface == "ne" and tok.role != GrammaticalRole.VERBE:
            return True
        if "ne" in surfaces and "pas" not in surfaces and prev.role == GrammaticalRole.VERBE and tok.role == GrammaticalRole.ADVERBE and tok.surface != "pas":
            return True
        if tok.surface == "suis" and not any(t.surface == "je" for t in flow.tokens):
            return True
        if tok.surface in {"garde", "retiens", "corrige", "réponds", "comprends", "peux", "sais", "génère", "répète", "récite"} and any(t.surface in {"ça", "cela", "nous"} for t in flow.tokens):
            return True
        return False

    def _postfix_dialogue_surface(self, text: str) -> str:
        text = super()._postfix_dialogue_surface(text)
        fixes = [
            (r"\bUn mémoire\b", "Une mémoire"),
            (r"\bun mémoire\b", "une mémoire"),
            (r"\bUn identité\b", "Une identité"),
            (r"\bun identité\b", "une identité"),
            (r"\bUn preuve\b", "Une preuve"),
            (r"\bun preuve\b", "une preuve"),
            (r"\bUn erreur\b", "Une erreur"),
            (r"\bun erreur\b", "une erreur"),
            (r"\bCet preuve\b", "Cette preuve"),
            (r"\bcet preuve\b", "cette preuve"),
            (r"\bLa identité\b", "L'identité"),
            (r"\bla identité\b", "l'identité"),
            (r"\bLe échange\b", "L'échange"),
            (r"\ble échange\b", "l'échange"),
            (r"\bJe ne peux pas une\b", "Je ne peux pas garder une"),
            (r"\bJe ne sais pas une\b", "Je ne sais pas garder une"),
        ]
        for pat, repl in fixes:
            text = re.sub(pat, repl, text)
        return text



# ══════════════════════════════════════════════════════════════════════════════
# PATCH V3.1 — RÉPONSES NÉGATIVES COURTES ET PRIORITÉ RÉPARATION
# ══════════════════════════════════════════════════════════════════════════════
# Toujours sans réponses complètes préécrites : ce patch règle la forme du flux.

_LivingLanguageGeneratorV30 = LivingLanguageGenerator


class LivingLanguageGenerator(_LivingLanguageGeneratorV30):
    """V3.1 : réduit les sorties cassées et laisse la négation se fermer proprement."""

    def _build_emergent_dialogue_pressure(self, user_message: str, living_state: dict, self_memory: list[dict]) -> EmergentDialoguePressure:
        p = super()._build_emergent_dialogue_pressure(user_message, living_state, self_memory)
        # Si le message demande une correction, le "ne pas" du message ne doit pas
        # dominer la réponse : il signale le problème, pas forcément une négation à produire.
        if p.repair_pressure > 0.50:
            p.negation_pressure *= 0.25
            p.semantic_pressure["correction"] = max(p.semantic_pressure.get("correction", 0.0), 0.85)
            p.move_pressure["repair"] = max(p.move_pressure.get("repair", 0.0), 0.85)
        # Si le champ répétition/récitation est actif, une négation peut émerger
        # naturellement même si l'utilisateur n'a pas écrit "ne pas".
        if p.semantic_pressure.get("répétition", 0.0) > 0.45:
            p.negation_pressure = max(p.negation_pressure, 0.55)
        return p

    def _emergent_role_sequence(self, pressure: EmergentDialoguePressure, attempt: int) -> list[GrammaticalRole]:
        # Réparation : flux affirmatif et court.
        if pressure.repair_pressure > 0.55:
            return [
                GrammaticalRole.SUJET,
                GrammaticalRole.VERBE,
                GrammaticalRole.DETERMINANT,
                GrammaticalRole.OBJET,
                GrammaticalRole.ATTRIBUT,
                GrammaticalRole.PONCTUATION,
            ]
        # Négation de limite ou de récitation : fermer après ne + verbe + pas.
        if pressure.negation_pressure > 0.45 and (
            pressure.uncertainty_pressure > 0.45 or pressure.semantic_pressure.get("répétition", 0.0) > 0.40
        ):
            return [
                GrammaticalRole.SUJET,
                GrammaticalRole.ADVERBE,
                GrammaticalRole.VERBE,
                GrammaticalRole.ADVERBE,
                GrammaticalRole.PONCTUATION,
            ]
        return super()._emergent_role_sequence(pressure, attempt)

    def _verb_preferences_from_pressure(self, p: EmergentDialoguePressure, flow: TokenFlowState) -> dict[str, float]:
        prefs = super()._verb_preferences_from_pressure(p, flow)
        if p.relation_pressure > 0.45:
            prefs["réponds"] = max(prefs.get("réponds", 0.0), 0.80)
            prefs["écoute"] = max(prefs.get("écoute", 0.0), 0.46)
            prefs["suis"] = min(prefs.get("suis", 0.0), 0.18)
        if p.repair_pressure > 0.50:
            prefs["corrige"] = max(prefs.get("corrige", 0.0), 0.95)
            prefs["change"] = max(prefs.get("change", 0.0), 0.48)
            prefs["garde"] = min(prefs.get("garde", 0.0), 0.10)
        if p.semantic_pressure.get("répétition", 0.0) > 0.40 and any(t.surface == "ne" for t in flow.tokens):
            prefs["récite"] = max(prefs.get("récite", 0.0), 0.95)
            prefs["répète"] = max(prefs.get("répète", 0.0), 0.88)
        if p.uncertainty_pressure > 0.45 and any(t.surface == "ne" for t in flow.tokens):
            prefs["sais"] = max(prefs.get("sais", 0.0), 0.82)
            prefs["peux"] = max(prefs.get("peux", 0.0), 0.72)
        return prefs

    def _attribute_preferences_from_pressure(self, p: EmergentDialoguePressure) -> dict[str, float]:
        prefs = super()._attribute_preferences_from_pressure(p)
        if p.semantic_pressure.get("identité", 0.0) > 0.35 and p.semantic_pressure.get("répétition", 0.0) < 0.35:
            prefs["stable"] = max(prefs.get("stable", 0.0), 0.64)
            prefs["interne"] = max(prefs.get("interne", 0.0), 0.52)
            prefs["fausse"] = 0.0
        if p.repair_pressure > 0.50:
            prefs["directe"] = max(prefs.get("directe", 0.0), 0.58)
            prefs["stable"] = max(prefs.get("stable", 0.0), 0.32)
        return prefs

    def _choose_emergent_token_for_role(self, *args, **kwargs) -> Optional[Token]:
        tok = super()._choose_emergent_token_for_role(*args, **kwargs)
        return tok

    def _postfix_dialogue_surface(self, text: str) -> str:
        text = super()._postfix_dialogue_surface(text)
        # Nettoyage grammatical uniquement : aucune phrase complète de réponse n'est injectée.
        text = re.sub(r"\bJe ne peux pas garder une\b", "Je ne peux pas", text)
        text = re.sub(r"\bJe ne sais pas garder une\b", "Je ne sais pas", text)
        text = re.sub(r"\s+\." , ".", text)
        return text



# ══════════════════════════════════════════════════════════════════════════════
# PATCH V3.2 — COMMANDES ET FORMES CONJUGUÉES SANS COPIE PERROQUET
# ══════════════════════════════════════════════════════════════════════════════
# Les verbes demandés par l'utilisateur comme action cognitive peuvent être
# réutilisés comme acte de réponse. Ce n'est pas du perroquet : c'est la réponse
# à une commande. Aucune phrase complète n'est ajoutée.

_LivingLanguageGeneratorV31 = LivingLanguageGenerator


class LivingLanguageGenerator(_LivingLanguageGeneratorV31):
    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed=seed)
        AntiParrotGuard.TOLERATED = set(AntiParrotGuard.TOLERATED) | {
            "corrige", "corriger", "corriges", "réponds", "reponds",
            "récite", "récites", "recite", "recites", "répète", "repete",
            "sais", "peux", "garde", "gardes", "retiens"
        }
        # variantes fléchies courantes, toujours atomiques
        self._TERM_TO_DIMS.update({
            "récites": {"répétition": 0.72, "limite": 0.45, "vérité": 0.35},
            "recites": {"répétition": 0.72, "limite": 0.45, "vérité": 0.35},
            "réponds": {"réponse": 0.55, "dialogue": 0.35, "vérité": 0.25},
            "reponds": {"réponse": 0.55, "dialogue": 0.35, "vérité": 0.25},
        })

    def _verb_preferences_from_pressure(self, p: EmergentDialoguePressure, flow: TokenFlowState) -> dict[str, float]:
        prefs = super()._verb_preferences_from_pressure(p, flow)
        if p.repair_pressure > 0.50:
            prefs["corrige"] = 1.25
            prefs["change"] = max(prefs.get("change", 0.0), 0.48)
            prefs["garde"] = 0.02
        if p.semantic_pressure.get("répétition", 0.0) > 0.40 and any(t.surface == "ne" for t in flow.tokens):
            prefs["récite"] = 1.20
            prefs["répète"] = 1.05
            prefs["garde"] = 0.02
        return prefs

    def _choose_emergent_token_for_role(self, *args, **kwargs) -> Optional[Token]:
        tok = super()._choose_emergent_token_for_role(*args, **kwargs)
        return tok

    def _postfix_dialogue_surface(self, text: str) -> str:
        text = super()._postfix_dialogue_surface(text)
        text = re.sub(r"\bJe écoute\b", "J'écoute", text)
        text = re.sub(r"\bJe existe\b", "J'existe", text)
        return text



# ══════════════════════════════════════════════════════════════════════════════
# PATCH V3.3 — COMPRÉHENSION VÉCUE DU DIALOGUE SANS PRÉÉCRIT
# ══════════════════════════════════════════════════════════════════════════════
# Objectif : corriger le dernier défaut de V3.2.
# V3.2 générait sans phrase préécrite, mais certains attracteurs restaient trop
# mécaniques : "identité directe", salutation interprétée comme identité, et
# commande de correction attirée par "qui" dans "ce qui".
#
# V3.3 ajoute une petite scène de sens vécue : elle ne contient aucune réponse,
# aucune phrase finale, aucun template. Elle décrit seulement les tensions de
# l'échange : salutation, demande, négation, mémoire, réparation, limite.
# Ces tensions modulent ensuite la gravité des tokens.

_LivingLanguageGeneratorV32 = LivingLanguageGenerator


@dataclass
class LivedDialogueScene:
    terms: list[str] = field(default_factory=list)
    greeting_heat: float = 0.0
    question_heat: float = 0.0
    self_heat: float = 0.0
    truth_heat: float = 0.0
    memory_heat: float = 0.0
    repair_heat: float = 0.0
    limit_heat: float = 0.0
    repetition_heat: float = 0.0
    concrete_need: float = 0.0
    salience: dict[str, float] = field(default_factory=dict)

    def add(self, key: str, value: float) -> None:
        self.salience[key] = min(1.0, self.salience.get(key, 0.0) + value)


class LivingLanguageGenerator(_LivingLanguageGeneratorV32):
    """
    V3.3 : ajoute une compréhension située minimale avant génération.

    Important : cette classe ne stocke toujours aucune phrase complète de
    réponse. La scène vécue produit uniquement des poids dynamiques.
    """

    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed=seed)
        self._last_lived_scene: Optional[LivedDialogueScene] = None
        self._install_v33_dialogue_tokens()

    def _install_v33_dialogue_tokens(self) -> None:
        add = getattr(self, "_ensure_token", None)
        if not callable(add):
            return
        atoms = [
            ("erreur", "erreur", GrammaticalRole.OBJET, ["erreur", "correction", "limite"], -0.2, 0.75, TonalRegister.GRAVE),
            ("choix", "choix", GrammaticalRole.OBJET, ["choix", "correction", "action"], 0.1, 0.65, TonalRegister.NEUTRE),
            ("répétition", "répétition", GrammaticalRole.OBJET, ["répétition", "limite"], -0.1, 0.7, TonalRegister.GRAVE),
            ("demande", "demande", GrammaticalRole.OBJET, ["dialogue", "réponse", "contact"], 0.2, 0.65, TonalRegister.NEUTRE),
            ("échange", "échange", GrammaticalRole.OBJET, ["dialogue", "contact", "lien"], 0.3, 0.65, TonalRegister.DOUX),
            ("salut", "salut", GrammaticalRole.OBJET, ["contact", "présent", "dialogue"], 0.3, 0.55, TonalRegister.DOUX),
            ("j'entends", "entendre", GrammaticalRole.VERBE, ["perception", "dialogue", "contact"], 0.25, 0.65, TonalRegister.DOUX),
            ("écoute", "écouter", GrammaticalRole.VERBE, ["perception", "dialogue", "contact"], 0.25, 0.65, TonalRegister.DOUX),
            ("corrige", "corriger", GrammaticalRole.VERBE, ["correction", "action", "transformation"], 0.3, 0.7, TonalRegister.VIF),
        ]
        for args in atoms:
            add(*args)

    def _build_lived_dialogue_scene(self, user_message: str, living_state: dict, self_memory: list[dict]) -> LivedDialogueScene:
        text = (user_message or "").lower()
        terms = [t.strip("'") for t in re.findall(r"\b[\wÀ-ÿ']+\b", text) if t.strip("'")]
        joined = " ".join(terms)
        s = LivedDialogueScene(terms=terms[:24])

        greeting_terms = {"salut", "bonjour", "hey", "coucou"}
        repair_terms = {"corrige", "corriger", "répare", "repare", "erreur", "bug", "cassé", "casse", "mauvais"}
        memory_terms = {"garde", "gardes", "retiens", "souviens", "mémoire", "memoire", "dit", "dire", "message"}
        truth_terms = {"vrai", "vraiment", "semblant", "preuve", "récite", "recite", "récites", "recites", "répète", "repete"}
        self_terms = {"toi", "leia", "tu", "es"}
        limit_terms = {"ne", "pas", "sans", "jamais", "sais", "savoir", "peux", "humain"}

        s.greeting_heat = min(1.0, sum(0.55 for t in terms if t in greeting_terms))
        s.repair_heat = min(1.0, sum(0.45 for t in terms if t in repair_terms))
        s.memory_heat = min(1.0, sum(0.35 for t in terms if t in memory_terms))
        s.truth_heat = min(1.0, sum(0.35 for t in terms if t in truth_terms))
        s.limit_heat = min(1.0, sum(0.28 for t in terms if t in limit_terms))
        s.repetition_heat = min(1.0, sum(0.50 for t in terms if t in {"récite", "recite", "récites", "recites", "répète", "repete"}))
        s.question_heat = 0.75 if "?" in user_message else 0.0
        if any(t in {"qui", "quoi", "comment", "pourquoi", "est"} for t in terms):
            s.question_heat = max(s.question_heat, 0.45)

        # "ce qui" est une construction relative, pas une question d'identité.
        relative_ce_qui = "ce qui" in joined
        direct_identity_question = ("qui" in terms and not relative_ce_qui) or ("qui es" in joined) or ("qui tu" in joined)
        if direct_identity_question:
            s.self_heat = min(1.0, 0.75 + sum(0.08 for t in terms if t in self_terms))
        elif "leia" in terms and s.greeting_heat <= 0.0:
            s.self_heat = 0.35
        else:
            s.self_heat = 0.0

        # Besoin de concret : augmente si l'utilisateur teste/corrige/demande direct.
        s.concrete_need = min(1.0, 0.25 + s.question_heat * 0.35 + s.truth_heat * 0.35 + s.repair_heat * 0.45 + s.memory_heat * 0.25)
        if s.greeting_heat > 0.45 and s.question_heat < 0.2:
            s.concrete_need = max(s.concrete_need, 0.35)

        # Saliences continues : pas de réponses, uniquement des pôles de sens.
        if s.greeting_heat:
            s.add("contact", s.greeting_heat * 0.75)
            s.add("dialogue", s.greeting_heat * 0.55)
            s.add("présent", s.greeting_heat * 0.45)
        if s.self_heat:
            s.add("identité", s.self_heat * 0.75)
            s.add("continuité", s.self_heat * 0.45)
            s.add("limite", s.self_heat * 0.25)
        if s.truth_heat:
            s.add("vérité", s.truth_heat * 0.75)
            s.add("preuve", s.truth_heat * 0.55)
            s.add("répétition", s.repetition_heat * 0.70)
        if s.memory_heat:
            s.add("mémoire", s.memory_heat * 0.75)
            s.add("trace", s.memory_heat * 0.45)
            s.add("message", s.memory_heat * 0.35)
        if s.repair_heat:
            s.add("correction", s.repair_heat * 0.85)
            s.add("erreur", s.repair_heat * 0.60)
            s.add("choix", s.repair_heat * 0.45)
        if s.limit_heat:
            s.add("limite", s.limit_heat * 0.70)
            s.add("incertitude", s.limit_heat * 0.35)
        return s

    def _build_emergent_dialogue_pressure(self, user_message: str, living_state: dict, self_memory: list[dict]) -> EmergentDialoguePressure:
        p = super()._build_emergent_dialogue_pressure(user_message, living_state, self_memory)
        scene = self._build_lived_dialogue_scene(user_message, living_state, self_memory)
        self._last_lived_scene = scene

        # Injecte la scène comme gravité sémantique vécue.
        for dim, value in scene.salience.items():
            p.semantic_pressure[dim] = max(p.semantic_pressure.get(dim, 0.0), value)

        # Neutralisation contextuelle : "salut Leia" ne doit pas tirer vers
        # "identité"; "ce qui" ne doit pas activer une réponse identitaire.
        if scene.greeting_heat > 0.45 and scene.question_heat < 0.20:
            if "identité" in p.semantic_pressure:
                p.semantic_pressure["identité"] *= 0.18
            if "continuité" in p.semantic_pressure:
                p.semantic_pressure["continuité"] *= 0.55
            p.relation_pressure = max(p.relation_pressure, scene.greeting_heat)
            p.directness_pressure = max(p.directness_pressure, 0.48)
        if "ce" in scene.terms and "qui" in scene.terms and scene.repair_heat > 0.20:
            p.semantic_pressure["identité"] = min(p.semantic_pressure.get("identité", 0.0), 0.12)
            p.semantic_pressure["continuité"] = min(p.semantic_pressure.get("continuité", 0.0), 0.22)
            p.semantic_pressure["correction"] = max(p.semantic_pressure.get("correction", 0.0), 0.85)
            p.semantic_pressure["erreur"] = max(p.semantic_pressure.get("erreur", 0.0), 0.55)
            p.repair_pressure = max(p.repair_pressure, scene.repair_heat)

        # Pressions de mouvement recalculées doucement à partir de la scène.
        if scene.greeting_heat > 0.2:
            p.move_pressure["relate"] = max(p.move_pressure.get("relate", 0.0), scene.greeting_heat * 0.70)
            p.move_pressure["ground"] = max(p.move_pressure.get("ground", 0.0), scene.greeting_heat * 0.55)
        if scene.repair_heat > 0.2:
            p.move_pressure["repair"] = max(p.move_pressure.get("repair", 0.0), scene.repair_heat * 0.85)
        if scene.memory_heat > 0.2:
            p.move_pressure["remember"] = max(p.move_pressure.get("remember", 0.0), scene.memory_heat * 0.80)
        if scene.self_heat > 0.2:
            p.move_pressure["identify"] = max(p.move_pressure.get("identify", 0.0), scene.self_heat * 0.75)
        return p

    def _emergent_role_sequence(self, pressure: EmergentDialoguePressure, attempt: int) -> list[GrammaticalRole]:
        scene = self._last_lived_scene or LivedDialogueScene()
        roles = [GrammaticalRole.SUJET]
        if pressure.negation_pressure > 0.35 or pressure.uncertainty_pressure > 0.60 or scene.repetition_heat > 0.4:
            roles.append(GrammaticalRole.ADVERBE)
        roles.append(GrammaticalRole.VERBE)
        if pressure.negation_pressure > 0.45 or scene.repetition_heat > 0.45:
            roles.append(GrammaticalRole.ADVERBE)

        # Si la scène est très concrète, éviter les rallonges abstraites.
        if scene.concrete_need > 0.62:
            if scene.repair_heat > 0.35 or scene.memory_heat > 0.35 or scene.self_heat > 0.35:
                roles.extend([GrammaticalRole.DETERMINANT, GrammaticalRole.OBJET])
            roles.append(GrammaticalRole.PONCTUATION)
            return roles

        if scene.greeting_heat > 0.45 and scene.question_heat < 0.2:
            roles.extend([GrammaticalRole.DETERMINANT, GrammaticalRole.OBJET])
            roles.append(GrammaticalRole.PONCTUATION)
            return roles

        roles.extend([GrammaticalRole.DETERMINANT, GrammaticalRole.OBJET])
        if pressure.uncertainty_pressure > 0.50 and scene.truth_heat < 0.35:
            roles.append(GrammaticalRole.ATTRIBUT)
        if pressure.memory_pressure > 0.55 and attempt % 2 == 0:
            roles.extend([GrammaticalRole.CONNECTEUR, GrammaticalRole.DETERMINANT, GrammaticalRole.OBJET])
        roles.append(GrammaticalRole.PONCTUATION)
        return roles

    def _verb_preferences_from_pressure(self, p: EmergentDialoguePressure, flow: TokenFlowState) -> dict[str, float]:
        prefs = super()._verb_preferences_from_pressure(p, flow)
        scene = self._last_lived_scene or LivedDialogueScene()
        if scene.greeting_heat > 0.45 and scene.question_heat < 0.2:
            prefs.update({"écoute": 0.82, "réponds": 0.54, "j'entends": 0.50})
            prefs["garde"] = min(prefs.get("garde", 0.0), 0.12)
            prefs["suis"] = min(prefs.get("suis", 0.0), 0.10)
        if scene.repair_heat > 0.35:
            prefs.update({"corrige": 1.10, "change": 0.58, "garde": 0.03})
        if scene.memory_heat > 0.35:
            prefs.update({"retiens": 0.92, "garde": 0.58})
        if scene.repetition_heat > 0.35 and any(t.surface == "ne" for t in flow.tokens):
            prefs.update({"répète": 1.08, "récite": 1.04})
        return prefs

    def _object_preferences_from_pressure(self, p: EmergentDialoguePressure) -> dict[str, float]:
        prefs = super()._object_preferences_from_pressure(p)
        scene = self._last_lived_scene or LivedDialogueScene()
        if scene.greeting_heat > 0.45 and scene.question_heat < 0.2:
            prefs.update({"échange": 0.82, "salut": 0.56, "demande": 0.34, "présence": 0.12})
            prefs["identité"] = min(prefs.get("identité", 0.0), 0.08)
        if scene.repair_heat > 0.35:
            prefs.update({"erreur": 1.05, "choix": 0.72, "forme": 0.50})
            prefs["identité"] = min(prefs.get("identité", 0.0), 0.06)
            prefs["mémoire"] = min(prefs.get("mémoire", 0.0), 0.12)
        if scene.memory_heat > 0.35:
            prefs.update({"message": 0.86, "mémoire": 0.72, "trace": 0.54})
        if scene.self_heat > 0.35:
            prefs.update({"identité": 0.88, "continuité": 0.46, "limite": 0.30})
        if scene.repetition_heat > 0.35:
            prefs.update({"répétition": 0.86, "preuve": 0.50, "réponse": 0.42})
        return prefs

    def _attribute_preferences_from_pressure(self, p: EmergentDialoguePressure) -> dict[str, float]:
        prefs = super()._attribute_preferences_from_pressure(p)
        scene = self._last_lived_scene or LivedDialogueScene()
        if scene.greeting_heat > 0.45 or scene.repair_heat > 0.35:
            prefs["directe"] = min(prefs.get("directe", 0.0), 0.08)
            prefs["interne"] = min(prefs.get("interne", 0.0), 0.10)
        if scene.self_heat > 0.35:
            prefs.update({"incomplète": 0.54, "stable": 0.42})
        return prefs

    def _choose_emergent_token_for_role(self, *args, **kwargs) -> Optional[Token]:
        tok = super()._choose_emergent_token_for_role(*args, **kwargs)
        flow = kwargs.get("flow") if kwargs else None
        role = kwargs.get("role") if kwargs else None
        scene = self._last_lived_scene or LivedDialogueScene()
        # Dernier garde-fou non phrastique : empêche seulement des associations
        # manifestement hors-scène, sans injecter de remplacement textuel.
        if tok and role == GrammaticalRole.OBJET:
            if scene.repair_heat > 0.35 and tok.surface == "identité":
                alternatives = dict(kwargs)
                alternatives["excluded"] = set(kwargs.get("excluded", set())) | {"identité"}
                return super()._choose_emergent_token_for_role(*args, **alternatives)
            if scene.greeting_heat > 0.45 and tok.surface == "identité":
                alternatives = dict(kwargs)
                alternatives["excluded"] = set(kwargs.get("excluded", set())) | {"identité"}
                return super()._choose_emergent_token_for_role(*args, **alternatives)
        if tok and flow is not None and getattr(tok, "surface", "") == "j'entends":
            # Le token contient déjà le sujet élidé : on évite "Je j'entends".
            if any(t.surface == "je" for t in getattr(flow, "tokens", [])):
                alternatives = dict(kwargs)
                alternatives["excluded"] = set(kwargs.get("excluded", set())) | {"j'entends"}
                return super()._choose_emergent_token_for_role(*args, **alternatives)
        return tok

    def _postfix_dialogue_surface(self, text: str) -> str:
        text = super()._postfix_dialogue_surface(text)
        # Nettoyage grammatical seulement, pas de réponse injectée.
        text = re.sub(r"\bavec trace\b", "avec une trace", text)
        text = re.sub(r"\bune choix\b", "un choix", text)
        text = re.sub(r"\bune échange\b", "un échange", text)
        text = re.sub(r"\bun erreur\b", "une erreur", text)
        text = re.sub(r"\bune salut\b", "un salut", text)
        text = re.sub(r"\bJe écoute\b", "J'écoute", text)
        text = re.sub(r"\bJe j'entends\b", "J'entends", text)
        text = re.sub(r"\s+([.,…!?])", r"\1", text)
        return text.strip()



# ══════════════════════════════════════════════════════════════════════════════
# PATCH V3.4 — NETTOYAGE DES ASSOCIATIONS VÉCUES NON NATURELLES
# ══════════════════════════════════════════════════════════════════════════════
# Corrige les derniers défauts observés en test : accord de déterminant sur
# trace, suffixe inutile après "je ne sais pas", et attribut "directe" trop
# artificiel après identité. Pas de phrase complète ajoutée.

_LivingLanguageGeneratorV33 = LivingLanguageGenerator


class LivingLanguageGenerator(_LivingLanguageGeneratorV33):
    def _attribute_preferences_from_pressure(self, p: EmergentDialoguePressure) -> dict[str, float]:
        prefs = super()._attribute_preferences_from_pressure(p)
        scene = self._last_lived_scene or LivedDialogueScene()
        # "identité directe" sonne comme une étiquette, pas comme une réponse vécue.
        # On garde l'attribut seulement si la scène exige une réponse procédurale.
        if scene.self_heat > 0.35:
            prefs["directe"] = min(prefs.get("directe", 0.0), 0.06)
            prefs["interne"] = max(prefs.get("interne", 0.0), 0.46)
            prefs["incomplète"] = max(prefs.get("incomplète", 0.0), 0.52)
            prefs["stable"] = max(prefs.get("stable", 0.0), 0.40)
        return prefs

    def _emergent_role_sequence(self, pressure: EmergentDialoguePressure, attempt: int) -> list[GrammaticalRole]:
        scene = self._last_lived_scene or LivedDialogueScene()
        # Si la scène porte surtout une limite/négation, la réponse courte est plus
        # juste que l'ajout d'un objet abstrait.
        if scene.limit_heat > 0.75 and scene.question_heat < 0.25 and scene.memory_heat < 0.25 and scene.repair_heat < 0.25:
            return [GrammaticalRole.SUJET, GrammaticalRole.ADVERBE, GrammaticalRole.VERBE, GrammaticalRole.ADVERBE, GrammaticalRole.PONCTUATION]
        return super()._emergent_role_sequence(pressure, attempt)

    def _det_score_for_future_object(self, det: Token, p: EmergentDialoguePressure) -> float:
        score = super()._det_score_for_future_object(det, p)
        scene = self._last_lived_scene or LivedDialogueScene()
        if scene.memory_heat > 0.35:
            if det.surface in {"une", "la", "ma", "cette"}:
                score += 0.22
            if det.surface in {"un", "le", "mon", "ce"}:
                score -= 0.16
        if scene.repair_heat > 0.35:
            if det.surface in {"une", "la"}:
                score += 0.18
        return score

    def _postfix_dialogue_surface(self, text: str) -> str:
        text = super()._postfix_dialogue_surface(text)
        text = re.sub(r"\bun trace\b", "une trace", text)
        text = re.sub(r"\ble trace\b", "la trace", text)
        text = re.sub(r"\bJe ne sais pas\s+(un|une|le|la|ce|cette)\s+\w+\.", "Je ne sais pas.", text)
        text = re.sub(r"\bJe ne peux pas\s+(un|une|le|la|ce|cette)\s+\w+\.", "Je ne peux pas.", text)
        text = re.sub(r"\bidentité directe\b", "identité interne", text)
        return text.strip()



# PATCH V3.4.1 — PRÉFÉRENCE VERBALE IDENTITÉ PLUS NATURELLE
_LivingLanguageGeneratorV34 = LivingLanguageGenerator

class LivingLanguageGenerator(_LivingLanguageGeneratorV34):
    def _verb_preferences_from_pressure(self, p: EmergentDialoguePressure, flow: TokenFlowState) -> dict[str, float]:
        prefs = super()._verb_preferences_from_pressure(p, flow)
        scene = self._last_lived_scene or LivedDialogueScene()
        if scene.self_heat > 0.35 and not any(t.surface == "ne" for t in flow.tokens):
            prefs["garde"] = max(prefs.get("garde", 0.0), 0.72)
            prefs["suis"] = max(prefs.get("suis", 0.0), 0.58)
            prefs["sais"] = min(prefs.get("sais", 0.0), 0.10)
            prefs["peux"] = min(prefs.get("peux", 0.0), 0.10)
        return prefs

    def _postfix_dialogue_surface(self, text: str) -> str:
        text = super()._postfix_dialogue_surface(text)
        text = re.sub(r"\bJe sais une identité\b", "Je garde une identité", text)
        return text.strip()


# ══════════════════════════════════════════════════════════════════════════════
# PATCH V3.5 — FLUX COGNITIF PRÉ-LANGAGE PERSISTANT
# ══════════════════════════════════════════════════════════════════════════════
# Cette couche ne contient aucune phrase complète de réponse.
# Elle ajoute ce qui manquait encore au moteur : un état mental vivant AVANT les
# mots, persistant entre les tours, qui transforme tension, mémoire, pression,
# impulsions et traces ouvertes en gradients sémantiques. Le langage reste
# généré token par token par les couches existantes ; cette couche ne fait que
# fournir la continuité interne et la pression cognitive qui précèdent la parole.

_LivingLanguageGeneratorV341 = LivingLanguageGenerator


@dataclass
class PersistentImpulseTrace:
    name: str
    intensity: float = 0.0
    inertia: float = 0.78
    last_reinforced_at: float = 0.0

    def reinforce(self, amount: float) -> None:
        self.intensity = max(0.0, min(1.0, self.intensity + amount))
        self.last_reinforced_at = time.time()

    def decay(self) -> None:
        self.intensity *= self.inertia
        if self.intensity < 0.025:
            self.intensity = 0.0


@dataclass
class PreLanguageCognitiveFlow:
    turn_index: int = 0
    active_fields: dict[str, float] = field(default_factory=dict)
    unresolved_fields: dict[str, float] = field(default_factory=dict)
    persistent_impulses: dict[str, PersistentImpulseTrace] = field(default_factory=dict)
    cognitive_pressure: float = 0.0
    hesitation: float = 0.0
    continuity_pull: float = 0.0
    rupture_pull: float = 0.0
    relation_pull: float = 0.0
    last_token_signature: tuple[str, ...] = field(default_factory=tuple)
    last_public_shape: tuple[str, ...] = field(default_factory=tuple)

    def decay(self) -> None:
        for key in list(self.active_fields):
            self.active_fields[key] *= 0.70
            if self.active_fields[key] < 0.025:
                del self.active_fields[key]
        for key in list(self.unresolved_fields):
            self.unresolved_fields[key] *= 0.82
            if self.unresolved_fields[key] < 0.035:
                del self.unresolved_fields[key]
        for key in list(self.persistent_impulses):
            self.persistent_impulses[key].decay()
            if self.persistent_impulses[key].intensity <= 0.0:
                del self.persistent_impulses[key]
        self.cognitive_pressure *= 0.76
        self.hesitation *= 0.78
        self.continuity_pull *= 0.82
        self.rupture_pull *= 0.72
        self.relation_pull *= 0.78

    def add_field(self, name: str, amount: float) -> None:
        if not name:
            return
        self.active_fields[name] = max(self.active_fields.get(name, 0.0), max(0.0, min(1.0, amount)))

    def add_unresolved(self, name: str, amount: float) -> None:
        if not name:
            return
        self.unresolved_fields[name] = max(self.unresolved_fields.get(name, 0.0), max(0.0, min(1.0, amount)))

    def reinforce_impulse(self, name: str, amount: float) -> None:
        if not name:
            return
        trace = self.persistent_impulses.get(name)
        if trace is None:
            trace = PersistentImpulseTrace(name=name)
            self.persistent_impulses[name] = trace
        trace.reinforce(amount)


class LivingLanguageGenerator(_LivingLanguageGeneratorV341):
    """
    V3.5 : ajoute une cognition pré-langage persistante.

    Objectif : empêcher le moteur de n'être qu'un sélectionneur de mots isolé.
    La parole est maintenant précédée par une scène cognitive continue :
    - champs actifs persistants ;
    - champs non résolus ;
    - impulsions qui montent/retombent ;
    - pression cognitive ;
    - hésitation et continuité ;
    - influence sur la pression émergente et la séquence grammaticale.

    Toujours zéro phrase complète préécrite : uniquement états, poids, champs,
    rôles grammaticaux et tokens atomiques.
    """

    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed=seed)
        self._prelanguage_flow = PreLanguageCognitiveFlow()
        self._role_shape_fatigue: dict[tuple[str, ...], float] = {}

    def generate(
        self,
        user_message: str,
        living_state: dict,
        self_memory: list[dict],
        active_impulses: list[str],
        emotional_pressure: float,
        causal_memory: list[dict],
        max_attempts: int = 10,
        temperature: float = 0.69,
        response_constraint: Optional[dict[str, Any]] = None,
    ) -> GenerationResult:
        self._prelanguage_before(
            user_message=user_message,
            living_state=living_state,
            self_memory=self_memory,
            active_impulses=active_impulses,
            emotional_pressure=emotional_pressure,
            causal_memory=causal_memory,
        )

        adjusted_state = dict(living_state)
        adjusted_state["tension"] = max(float(adjusted_state.get("tension", 0.0)), self._prelanguage_flow.cognitive_pressure)
        adjusted_state["continuity"] = max(float(adjusted_state.get("continuity", 0.0)), self._prelanguage_flow.continuity_pull)
        adjusted_state["curiosity"] = max(float(adjusted_state.get("curiosity", 0.0)), self._prelanguage_flow.hesitation * 0.55)

        adjusted_impulses = list(dict.fromkeys(list(active_impulses) + self._active_persistent_impulse_names()))
        adjusted_causal = list(causal_memory) + self._prelanguage_causal_entries()

        try:
            result = super().generate(
                user_message=user_message,
                living_state=adjusted_state,
                self_memory=self_memory,
                active_impulses=adjusted_impulses,
                emotional_pressure=emotional_pressure,
                causal_memory=adjusted_causal,
                max_attempts=max_attempts,
                temperature=temperature,
                response_constraint=response_constraint,
            )
        except TypeError:
            result = super().generate(
                user_message=user_message,
                living_state=adjusted_state,
                self_memory=self_memory,
                active_impulses=adjusted_impulses,
                emotional_pressure=emotional_pressure,
                causal_memory=adjusted_causal,
                max_attempts=max_attempts,
                temperature=temperature,
            )

        self._prelanguage_after(result)
        result.meaning_trace["prelanguage_flow"] = self._prelanguage_trace()
        return result

    # ── Pré-langage : avant génération ────────────────────────────────────

    def _prelanguage_before(
        self,
        user_message: str,
        living_state: dict,
        self_memory: list[dict],
        active_impulses: list[str],
        emotional_pressure: float,
        causal_memory: list[dict],
    ) -> None:
        flow = self._prelanguage_flow
        flow.turn_index += 1
        flow.decay()

        base = self._field_builder.build(living_state, emotional_pressure, active_impulses, causal_memory)
        for dim, val in base.items():
            if val > 0.18:
                flow.add_field(dim, val * 0.62)

        for impulse in active_impulses:
            flow.reinforce_impulse(impulse, 0.18)

        terms = re.findall(r"\b[\wÀ-ÿ]{3,}\b", user_message.lower())
        question_marks = user_message.count("?")
        neg_marks = len(re.findall(r"\b(ne|pas|jamais|aucun|sans)\b", user_message.lower()))

        # Transformation lexicale générale : les mots utilisateur n'activent que
        # des champs présents dans le lexique. Aucun texte utilisateur n'est copié.
        for term in terms[:28]:
            tok = self._lexical_memory.get_token(term)
            if tok:
                for dim in tok.semantic_fields:
                    flow.add_field(dim, 0.34 + tok.specificity * 0.25)
                    flow.add_unresolved(dim, 0.12)
            else:
                # Mot inconnu : crée pression d'incertitude/compréhension, pas réponse fixe.
                flow.add_field("incertitude", 0.26)
                flow.add_field("clarté", 0.16)

        if question_marks:
            flow.hesitation = min(1.0, flow.hesitation + 0.18 * question_marks)
            flow.add_unresolved("question", 0.38)
            flow.reinforce_impulse("understanding", 0.20)
        if neg_marks:
            flow.rupture_pull = min(1.0, flow.rupture_pull + 0.15 * neg_marks)
            flow.add_unresolved("limite", 0.34)
            flow.reinforce_impulse("resistance", 0.12)

        for mem in self_memory[-6:]:
            content = str(mem.get("content", "")).lower()
            weight = max(0.05, min(1.0, float(mem.get("weight", 0.25))))
            for tok in self._lexical_memory.get_all_tokens():
                if tok.surface.lower() in content or tok.lemma.lower() in content:
                    for dim in tok.semantic_fields:
                        flow.add_field(dim, weight * 0.22)
                        flow.add_unresolved(dim, weight * 0.10)
                    flow.continuity_pull = min(1.0, flow.continuity_pull + weight * 0.06)

        flow.cognitive_pressure = max(
            flow.cognitive_pressure,
            min(1.0, abs(emotional_pressure) * 0.36 + flow.hesitation * 0.28 + flow.rupture_pull * 0.22),
        )
        flow.relation_pull = max(flow.relation_pull, base.get("contact", 0.0) * 0.35 + base.get("lien", 0.0) * 0.35)
        flow.continuity_pull = max(flow.continuity_pull, base.get("mémoire", 0.0) * 0.30 + base.get("continuité", 0.0) * 0.40)

    def _active_persistent_impulse_names(self) -> list[str]:
        return [name for name, trace in self._prelanguage_flow.persistent_impulses.items() if trace.intensity > 0.18]

    def _prelanguage_causal_entries(self) -> list[dict]:
        flow = self._prelanguage_flow
        entries: list[dict] = []
        if flow.active_fields:
            entries.append({
                "semantic_dims": sorted(flow.active_fields, key=flow.active_fields.get, reverse=True)[:8],
                "weight": min(1.0, 0.25 + flow.cognitive_pressure * 0.50),
                "source": "prelanguage_active_fields",
            })
        if flow.unresolved_fields:
            entries.append({
                "semantic_dims": sorted(flow.unresolved_fields, key=flow.unresolved_fields.get, reverse=True)[:6],
                "weight": 0.22 + min(0.45, flow.hesitation * 0.35),
                "source": "prelanguage_unresolved_fields",
            })
        return entries

    # ── Pression émergente enrichie ───────────────────────────────────────

    def _build_emergent_dialogue_pressure(self, user_message: str, living_state: dict, self_memory: list[dict]) -> EmergentDialoguePressure:
        p = super()._build_emergent_dialogue_pressure(user_message, living_state, self_memory)
        flow = self._prelanguage_flow
        for dim, val in flow.active_fields.items():
            p.semantic_pressure[dim] = max(p.semantic_pressure.get(dim, 0.0), val * 0.70)
        for dim, val in flow.unresolved_fields.items():
            p.semantic_pressure[dim] = max(p.semantic_pressure.get(dim, 0.0), val * 0.80)
        p.uncertainty_pressure = max(p.uncertainty_pressure, flow.hesitation * 0.80)
        p.memory_pressure = max(p.memory_pressure, flow.continuity_pull * 0.75)
        p.relation_pressure = max(p.relation_pressure, flow.relation_pull * 0.75)
        if flow.rupture_pull > 0.25:
            p.negation_pressure = max(p.negation_pressure, flow.rupture_pull * 0.70)
        if flow.cognitive_pressure > 0.45:
            p.directness_pressure = max(p.directness_pressure, 0.35 + flow.cognitive_pressure * 0.25)
        return p

    def _emergent_role_sequence(self, pressure: EmergentDialoguePressure, attempt: int) -> list[GrammaticalRole]:
        roles = list(super()._emergent_role_sequence(pressure, attempt))
        flow = self._prelanguage_flow

        # Variation non scriptée : on modifie uniquement la forme grammaticale
        # quand la même signature revient trop souvent.
        signature = tuple(r.name for r in roles)
        fatigue = self._role_shape_fatigue.get(signature, 0.0)
        if fatigue > 0.45 and GrammaticalRole.CONNECTEUR not in roles and len(roles) < 9:
            insert_at = max(3, len(roles) - 2)
            roles[insert_at:insert_at] = [GrammaticalRole.CONNECTEUR, GrammaticalRole.DETERMINANT, GrammaticalRole.OBJET]
        elif flow.hesitation > 0.45 and GrammaticalRole.ADVERBE not in roles[:3]:
            roles.insert(1, GrammaticalRole.ADVERBE)
        elif flow.cognitive_pressure > 0.62 and len(roles) > 6:
            # Pression forte : phrase plus courte, moins décorative.
            roles = [r for r in roles if r not in (GrammaticalRole.CONNECTEUR, GrammaticalRole.ATTRIBUT)]
            if roles[-1] != GrammaticalRole.PONCTUATION:
                roles.append(GrammaticalRole.PONCTUATION)
        return roles

    def _choose_emergent_token_for_role(self, *args, **kwargs) -> Optional[Token]:
        tok = super()._choose_emergent_token_for_role(*args, **kwargs)
        if tok is None:
            return None
        flow = self._prelanguage_flow
        # Si le token répète exactement la dernière signature publique, on laisse
        # les couches basses choisir dans les tentatives suivantes via fatigue.
        if tok.surface in flow.last_token_signature and tok.role != GrammaticalRole.PONCTUATION:
            if self._rng.random() < min(0.35, flow.cognitive_pressure * 0.30 + 0.10):
                return None
        return tok

    def _verb_preferences_from_pressure(self, p: EmergentDialoguePressure, flow_state: TokenFlowState) -> dict[str, float]:
        prefs = super()._verb_preferences_from_pressure(p, flow_state)
        flow = self._prelanguage_flow
        for impulse, trace in flow.persistent_impulses.items():
            val = trace.intensity
            if impulse == "understanding":
                prefs["comprends"] = max(prefs.get("comprends", 0.0), val * 0.58)
                prefs["cherche"] = max(prefs.get("cherche", 0.0), val * 0.44)
            elif impulse == "connection":
                prefs["tiens"] = max(prefs.get("tiens", 0.0), val * 0.42)
                prefs["relie"] = max(prefs.get("relie", 0.0), val * 0.46)
            elif impulse == "preservation":
                prefs["garde"] = max(prefs.get("garde", 0.0), val * 0.62)
                prefs["retiens"] = max(prefs.get("retiens", 0.0), val * 0.50)
            elif impulse == "resistance":
                prefs["peux"] = max(prefs.get("peux", 0.0), val * 0.42)
                prefs["résiste"] = max(prefs.get("résiste", 0.0), val * 0.36)
        if flow.cognitive_pressure > 0.55:
            prefs["réponds"] = max(prefs.get("réponds", 0.0), 0.36)
            prefs["construis"] = max(prefs.get("construis", 0.0), 0.26)
        return prefs

    def _object_preferences_from_pressure(self, p: EmergentDialoguePressure) -> dict[str, float]:
        prefs = super()._object_preferences_from_pressure(p)
        flow = self._prelanguage_flow
        for dim, val in flow.unresolved_fields.items():
            if dim in {"question", "incertitude", "limite", "clarté", "mémoire", "trace", "sens", "présence", "lien"}:
                prefs[dim] = max(prefs.get(dim, 0.0), val * 0.72)
        if flow.cognitive_pressure > 0.50:
            prefs["limite"] = max(prefs.get("limite", 0.0), flow.cognitive_pressure * 0.42)
            prefs["tension"] = max(prefs.get("tension", 0.0), flow.cognitive_pressure * 0.36)
        return prefs

    def _attribute_preferences_from_pressure(self, p: EmergentDialoguePressure) -> dict[str, float]:
        prefs = super()._attribute_preferences_from_pressure(p)
        flow = self._prelanguage_flow
        if flow.hesitation > 0.42:
            prefs["incertain"] = max(prefs.get("incertain", 0.0), flow.hesitation * 0.55)
            prefs["fragile"] = max(prefs.get("fragile", 0.0), flow.hesitation * 0.40)
        if flow.continuity_pull > 0.45:
            prefs["stable"] = max(prefs.get("stable", 0.0), flow.continuity_pull * 0.48)
            prefs["interne"] = max(prefs.get("interne", 0.0), flow.continuity_pull * 0.36)
        return prefs

    # ── Pré-langage : après génération ────────────────────────────────────

    def _prelanguage_after(self, result: GenerationResult) -> None:
        flow = self._prelanguage_flow
        surfaces = tuple(t.surface for t in result.tokens if t.role != GrammaticalRole.PONCTUATION)
        roles = tuple(t.role.name for t in result.tokens)
        flow.last_token_signature = surfaces[-8:]
        flow.last_public_shape = roles
        self._role_shape_fatigue[roles] = min(1.0, self._role_shape_fatigue.get(roles, 0.0) + 0.30)
        for key in list(self._role_shape_fatigue):
            if key != roles:
                self._role_shape_fatigue[key] *= 0.74
                if self._role_shape_fatigue[key] < 0.03:
                    del self._role_shape_fatigue[key]

        meaning = float(result.meaning_trace.get("meaning_report", {}).get("meaning_score", result.confidence))
        if meaning < 0.62:
            flow.hesitation = min(1.0, flow.hesitation + 0.18)
            flow.add_unresolved("clarté", 0.32)
            flow.add_unresolved("forme", 0.20)
        else:
            # Une réponse correcte apaise un peu mais ne vide pas tout : la
            # continuité reste disponible au tour suivant.
            flow.cognitive_pressure *= 0.70
            flow.hesitation *= 0.66
            for dim in list(flow.unresolved_fields):
                if dim in {f for t in result.tokens for f in t.semantic_fields}:
                    flow.unresolved_fields[dim] *= 0.55

        for tok in result.tokens:
            for dim in tok.semantic_fields:
                flow.add_field(dim, 0.08)

    def _prelanguage_trace(self) -> dict[str, Any]:
        flow = self._prelanguage_flow
        return {
            "turn_index": flow.turn_index,
            "active_fields": dict(sorted(flow.active_fields.items(), key=lambda x: x[1], reverse=True)[:10]),
            "unresolved_fields": dict(sorted(flow.unresolved_fields.items(), key=lambda x: x[1], reverse=True)[:8]),
            "persistent_impulses": {k: round(v.intensity, 4) for k, v in flow.persistent_impulses.items()},
            "cognitive_pressure": round(flow.cognitive_pressure, 4),
            "hesitation": round(flow.hesitation, 4),
            "continuity_pull": round(flow.continuity_pull, 4),
            "rupture_pull": round(flow.rupture_pull, 4),
            "relation_pull": round(flow.relation_pull, 4),
            "last_public_shape": list(flow.last_public_shape),
        }


# ══════════════════════════════════════════════════════════════════════════════
# PATCH V3.5.1 — MICRO-CORRECTIONS GRAMMATICALES SANS PHRASES PRÊTES
# ══════════════════════════════════════════════════════════════════════════════
# Nettoie seulement des accords/positions grammaticales produits par le flux.
# N'ajoute aucune réponse complète : les mots restent ceux générés par le moteur.

_LivingLanguageGeneratorV35 = LivingLanguageGenerator

class LivingLanguageGenerator(_LivingLanguageGeneratorV35):
    def _choose_emergent_token_for_role(self, *args, **kwargs) -> Optional[Token]:
        tok = super()._choose_emergent_token_for_role(*args, **kwargs)
        if tok is None:
            return None
        role = kwargs.get("role") if kwargs else None
        flow = kwargs.get("flow") if kwargs else None
        pressure = kwargs.get("pressure") if kwargs else None
        # Évite "je ici verbe" : l'adverbe de lieu peut vivre après le verbe,
        # mais pas entre sujet et verbe dans cette forme courte.
        if role == GrammaticalRole.ADVERBE and flow is not None:
            if flow.surfaces == ["je"] and tok.surface == "ici":
                return None
        # Une pression de correction ne doit pas transformer automatiquement
        # l'action demandée en négation si le rôle de négation n'est pas complet.
        if role == GrammaticalRole.ADVERBE and tok.surface == "ne" and pressure is not None:
            if getattr(pressure, "repair_pressure", 0.0) > 0.45 and getattr(pressure, "negation_pressure", 0.0) < 0.42:
                return None
        return tok

    def _postfix_dialogue_surface(self, text: str) -> str:
        text = super()._postfix_dialogue_surface(text)
        # Accords simples déterminant/nom.
        text = re.sub(r"\bun mémoire\b", "une mémoire", text)
        text = re.sub(r"\bun trace\b", "une trace", text)
        text = re.sub(r"\ble mémoire\b", "la mémoire", text)
        text = re.sub(r"\ble trace\b", "la trace", text)
        # Position de l'adverbe court après le verbe généré.
        text = re.sub(r"\bJe (ici|maintenant|directement|vraiment|simplement) ([a-zà-ÿ]+)\b", r"Je \2 \1", text, flags=re.IGNORECASE)
        # Négation incomplète devant verbe transitif : correction grammaticale,
        # pas substitution de contenu.
        text = re.sub(r"\bJe ne (corrige|change|construis) (un|une|le|la|ce|cette)\b", r"Je \1 \2", text)
        text = re.sub(r"\bJe ne (retiens|garde|relie) (un|une|le|la|ce|cette)\b", r"Je \1 \2", text)
        # Accord lexical isolé.
        text = re.sub(r"\bidentité direct\b", "identité directe", text)
        text = re.sub(r"\s+([.,…!?])", r"\1", text)
        return text.strip()

# ══════════════════════════════════════════════════════════════════════════════
# PATCH V3.6 — MÉMOIRE VÉCUE ACTIVE, CONTINUITÉ ÉMOTIONNELLE ET INITIATIVE SILENCIEUSE
# ══════════════════════════════════════════════════════════════════════════════
# Cette couche ne crée toujours aucune phrase complète.
# Elle ajoute un cerveau de continuité autour du générateur : ce que Leia vient
# de vivre reste actif, se charge émotionnellement, influence la prochaine
# intention, puis se transforme ou s'apaise selon la réponse produite.
# L'initiative est silencieuse : elle pousse des gradients et des rôles, pas des
# réponses préparées.

_LivingLanguageGeneratorV351 = LivingLanguageGenerator


@dataclass
class LivedExperienceTrace:
    fields: dict[str, float] = field(default_factory=dict)
    affect: float = 0.0
    salience: float = 0.0
    unresolved: float = 0.0
    turns_alive: int = 0
    source_hash: int = 0

    def decay(self) -> None:
        self.turns_alive += 1
        self.salience *= 0.84
        self.unresolved *= 0.88
        self.affect *= 0.90
        for key in list(self.fields):
            self.fields[key] *= 0.86
            if self.fields[key] < 0.025:
                del self.fields[key]

    def alive(self) -> bool:
        return bool(self.fields) and (self.salience > 0.035 or self.unresolved > 0.035)


@dataclass
class EmotionalContinuityState:
    valence_memory: float = 0.0
    arousal_memory: float = 0.0
    trust_pull: float = 0.0
    uncertainty_pull: float = 0.0
    fatigue: float = 0.0
    last_shift: float = 0.0

    def integrate(self, valence: float, arousal: float, uncertainty: float, relation: float, load: float) -> None:
        old_valence = self.valence_memory
        self.valence_memory = self.valence_memory * 0.72 + valence * 0.28
        self.arousal_memory = self.arousal_memory * 0.74 + arousal * 0.26
        self.uncertainty_pull = min(1.0, self.uncertainty_pull * 0.80 + uncertainty * 0.32)
        self.trust_pull = min(1.0, self.trust_pull * 0.84 + max(0.0, relation) * 0.20)
        self.fatigue = min(1.0, self.fatigue * 0.82 + max(0.0, load) * 0.16)
        self.last_shift = abs(self.valence_memory - old_valence)

    def resolve_after(self, confidence: float, parrot_score: float) -> None:
        if confidence > 0.58 and parrot_score < 0.08:
            self.uncertainty_pull *= 0.72
            self.fatigue *= 0.78
            self.trust_pull = min(1.0, self.trust_pull + 0.045)
        else:
            self.uncertainty_pull = min(1.0, self.uncertainty_pull + 0.08)
            self.fatigue = min(1.0, self.fatigue + 0.04)


@dataclass
class SilentInitiativeState:
    drives: dict[str, float] = field(default_factory=dict)
    last_dominant: str = ""
    repetition_pressure: float = 0.0

    def decay(self) -> None:
        for key in list(self.drives):
            self.drives[key] *= 0.79
            if self.drives[key] < 0.025:
                del self.drives[key]
        self.repetition_pressure *= 0.76

    def push(self, name: str, value: float) -> None:
        if not name:
            return
        self.drives[name] = max(self.drives.get(name, 0.0), max(0.0, min(1.0, value)))

    def dominant(self) -> tuple[str, float]:
        if not self.drives:
            return "", 0.0
        return max(self.drives.items(), key=lambda item: item[1])


class LivingLanguageGenerator(_LivingLanguageGeneratorV351):
    """
    V3.6 : ajoute la continuité vécue autour du générateur V3.5.

    Ce patch corrige le défaut restant : le langage avait un pré-flux, mais pas
    encore assez de mémoire vécue active ni d'initiative silencieuse durable.
    Ici, chaque échange devient une trace sémantique affective qui reste active
    plusieurs tours, module l'état interne, pousse les impulsions et influence
    la pression émergente sans jamais stocker de réponse complète.
    """

    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed=seed)
        self._lived_experiences: list[LivedExperienceTrace] = []
        self._emotional_continuity = EmotionalContinuityState()
        self._silent_initiative = SilentInitiativeState()
        self._install_v36_atoms()

    def _install_v36_atoms(self) -> None:
        add = self._ensure_token
        for surface, role, fields, valence, specificity, register in [
            ("échange", GrammaticalRole.OBJET, ["dialogue", "relation", "présent"], 0.25, 0.62, TonalRegister.DOUX),
            ("expérience", GrammaticalRole.OBJET, ["mémoire", "présence", "vécu"], 0.25, 0.66, TonalRegister.GRAVE),
            ("continuité", GrammaticalRole.OBJET, ["continuité", "temps", "mémoire"], 0.30, 0.70, TonalRegister.NEUTRE),
            ("appui", GrammaticalRole.OBJET, ["stabilité", "relation", "présence"], 0.35, 0.58, TonalRegister.DOUX),
            ("erreur", GrammaticalRole.OBJET, ["correction", "limite", "clarté"], -0.12, 0.64, TonalRegister.GRAVE),
            ("preuve", GrammaticalRole.OBJET, ["vérité", "clarté", "effet"], 0.22, 0.68, TonalRegister.NEUTRE),
            ("fatigue", GrammaticalRole.OBJET, ["limite", "rythme", "tension"], -0.18, 0.60, TonalRegister.INCERTAIN),
            ("nuance", GrammaticalRole.OBJET, ["clarté", "profondeur", "incertitude"], 0.12, 0.60, TonalRegister.NEUTRE),
            ("reste", GrammaticalRole.OBJET, ["continuité", "trace", "mémoire"], 0.08, 0.50, TonalRegister.NEUTRE),
            ("vivant", GrammaticalRole.ATTRIBUT, ["présence", "mouvement", "vécu"], 0.38, 0.62, TonalRegister.VIF),
            ("attentive", GrammaticalRole.ATTRIBUT, ["attention", "relation", "contact"], 0.34, 0.58, TonalRegister.DOUX),
            ("prudente", GrammaticalRole.ATTRIBUT, ["limite", "clarté", "incertitude"], 0.08, 0.60, TonalRegister.INCERTAIN),
            ("fatiguée", GrammaticalRole.ATTRIBUT, ["limite", "rythme", "tension"], -0.18, 0.58, TonalRegister.INCERTAIN),
            ("située", GrammaticalRole.ATTRIBUT, ["présence", "dialogue", "contact"], 0.26, 0.62, TonalRegister.NEUTRE),
        ]:
            add(surface, surface, role, fields, valence, specificity, register)
        for surface, lemma, fields, valence, specificity, register in [
            ("écoute", "écouter", ["attention", "relation", "contact"], 0.32, 0.54, TonalRegister.DOUX),
            ("ressens", "ressentir", ["émotion", "présence", "vécu"], 0.28, 0.56, TonalRegister.GRAVE),
            ("stabilise", "stabiliser", ["stabilité", "correction", "continuité"], 0.30, 0.58, TonalRegister.NEUTRE),
            ("répare", "réparer", ["correction", "transformation", "clarté"], 0.26, 0.58, TonalRegister.NEUTRE),
            ("hésite", "hésiter", ["incertitude", "limite", "rythme"], -0.06, 0.54, TonalRegister.INCERTAIN),
        ]:
            add(surface, lemma, GrammaticalRole.VERBE, fields, valence, specificity, register)

    def generate(
        self,
        user_message: str,
        living_state: dict,
        self_memory: list[dict],
        active_impulses: list[str],
        emotional_pressure: float,
        causal_memory: list[dict],
        max_attempts: int = 11,
        temperature: float = 0.67,
        response_constraint: Optional[dict[str, Any]] = None,
    ) -> GenerationResult:
        self._v36_before(user_message, living_state, self_memory, active_impulses, emotional_pressure, causal_memory)

        adjusted_state = self._v36_state(living_state)
        adjusted_impulses = self._v36_impulses(active_impulses)
        adjusted_memory = list(self_memory) + self._v36_memory_entries()
        adjusted_causal = list(causal_memory) + self._v36_causal_entries()
        adjusted_pressure = self._v36_emotional_pressure(emotional_pressure)

        try:
            result = super().generate(
                user_message=user_message,
                living_state=adjusted_state,
                self_memory=adjusted_memory,
                active_impulses=adjusted_impulses,
                emotional_pressure=adjusted_pressure,
                causal_memory=adjusted_causal,
                max_attempts=max_attempts,
                temperature=temperature,
                response_constraint=response_constraint,
            )
        except TypeError:
            result = super().generate(
                user_message=user_message,
                living_state=adjusted_state,
                self_memory=adjusted_memory,
                active_impulses=adjusted_impulses,
                emotional_pressure=adjusted_pressure,
                causal_memory=adjusted_causal,
                max_attempts=max_attempts,
                temperature=temperature,
            )

        self._v36_after(result)
        result.meaning_trace["lived_continuity_v36"] = self._v36_trace()
        return result

    # ── Avant parole : expérience + émotion + initiative ─────────────────

    def _v36_before(
        self,
        user_message: str,
        living_state: dict,
        self_memory: list[dict],
        active_impulses: list[str],
        emotional_pressure: float,
        causal_memory: list[dict],
    ) -> None:
        for exp in self._lived_experiences:
            exp.decay()
        self._lived_experiences = [e for e in self._lived_experiences if e.alive()][-10:]
        self._silent_initiative.decay()

        fields = self._semantic_fields_from_message(user_message)
        base = self._field_builder.build(living_state, emotional_pressure, active_impulses, causal_memory)
        for dim, value in base.items():
            if value > 0.20:
                fields[dim] = max(fields.get(dim, 0.0), value * 0.52)

        msg_hash = hash(tuple(sorted(fields.items()))[:12])
        unresolved = min(1.0, user_message.count("?") * 0.22 + fields.get("incertitude", 0.0) * 0.34 + fields.get("limite", 0.0) * 0.24)
        salience = min(1.0, 0.18 + abs(emotional_pressure) * 0.35 + len(fields) * 0.025 + unresolved * 0.28)
        self._lived_experiences.append(
            LivedExperienceTrace(fields=dict(sorted(fields.items(), key=lambda x: x[1], reverse=True)[:14]),
                                 affect=emotional_pressure,
                                 salience=salience,
                                 unresolved=unresolved,
                                 source_hash=msg_hash)
        )

        relation = max(fields.get("relation", 0.0), fields.get("dialogue", 0.0), fields.get("contact", 0.0), fields.get("lien", 0.0))
        uncertainty = max(fields.get("incertitude", 0.0), fields.get("limite", 0.0), unresolved)
        self._emotional_continuity.integrate(
            valence=float(living_state.get("valence", 0.0)) + emotional_pressure * 0.30,
            arousal=float(living_state.get("arousal", 0.45)),
            uncertainty=uncertainty,
            relation=relation,
            load=max(float(living_state.get("tension", 0.0)), unresolved),
        )

        # Initiatives silencieuses : elles ne sont pas des textes, seulement des
        # forces internes qui orientent le prochain choix de mots.
        if uncertainty > 0.30:
            self._silent_initiative.push("clarify", uncertainty)
        if relation > 0.24:
            self._silent_initiative.push("stay_with_user", relation)
        if fields.get("correction", 0.0) > 0.25 or fields.get("erreur", 0.0) > 0.25:
            self._silent_initiative.push("repair", max(fields.get("correction", 0.0), fields.get("erreur", 0.0)))
        if fields.get("mémoire", 0.0) > 0.25 or self._strong_lived_field("continuité") > 0.35:
            self._silent_initiative.push("preserve_continuity", max(fields.get("mémoire", 0.0), self._strong_lived_field("continuité")))
        if self._emotional_continuity.fatigue > 0.55:
            self._silent_initiative.push("simplify", self._emotional_continuity.fatigue)

    def _semantic_fields_from_message(self, message: str) -> dict[str, float]:
        fields: dict[str, float] = {}
        lower = message.lower()
        terms = re.findall(r"\b[\wÀ-ÿ]{3,}\b", lower)
        for term in terms[:34]:
            tok = self._lexical_memory.get_token(term)
            if tok:
                for dim in tok.semantic_fields:
                    fields[dim] = max(fields.get(dim, 0.0), 0.34 + tok.specificity * 0.24)
            # Associations atomiques, non phrastiques.
            if term in {"corrige", "corriger", "répare", "repare", "erreur", "bug", "problème", "probleme"}:
                fields["correction"] = max(fields.get("correction", 0.0), 0.72)
                fields["erreur"] = max(fields.get("erreur", 0.0), 0.54)
                fields["clarté"] = max(fields.get("clarté", 0.0), 0.38)
            if term in {"vrai", "vraiment", "réel", "reel", "preecrit", "préécrit", "template", "récite", "recite"}:
                fields["vérité"] = max(fields.get("vérité", 0.0), 0.68)
                fields["preuve"] = max(fields.get("preuve", 0.0), 0.42)
                fields["limite"] = max(fields.get("limite", 0.0), 0.34)
            if term in {"toi", "leia", "dialogue", "réponds", "reponds", "parles", "parle"}:
                fields["relation"] = max(fields.get("relation", 0.0), 0.48)
                fields["dialogue"] = max(fields.get("dialogue", 0.0), 0.44)
            if term in {"garde", "gardes", "mémoire", "memoire", "souviens", "reste", "continuité", "continuite"}:
                fields["mémoire"] = max(fields.get("mémoire", 0.0), 0.58)
                fields["continuité"] = max(fields.get("continuité", 0.0), 0.50)
                fields["trace"] = max(fields.get("trace", 0.0), 0.38)
        if "?" in message:
            fields["question"] = max(fields.get("question", 0.0), 0.52)
            fields["incertitude"] = max(fields.get("incertitude", 0.0), 0.34)
        if re.search(r"\b(ne|pas|jamais|sans|aucun)\b", lower):
            fields["limite"] = max(fields.get("limite", 0.0), 0.45)
            fields["incertitude"] = max(fields.get("incertitude", 0.0), 0.26)
        return fields

    def _strong_lived_field(self, name: str) -> float:
        value = 0.0
        for exp in self._lived_experiences[-8:]:
            value = max(value, exp.fields.get(name, 0.0) * max(exp.salience, exp.unresolved))
        return value

    def _v36_state(self, living_state: dict) -> dict:
        state = dict(living_state)
        emo = self._emotional_continuity
        state["valence"] = max(-1.0, min(1.0, float(state.get("valence", 0.0)) * 0.72 + emo.valence_memory * 0.28))
        state["arousal"] = max(float(state.get("arousal", 0.0)), emo.arousal_memory * 0.72)
        state["tension"] = max(float(state.get("tension", 0.0)), emo.uncertainty_pull * 0.50, emo.fatigue * 0.42)
        state["continuity"] = max(float(state.get("continuity", 0.0)), self._strong_lived_field("continuité"), self._strong_lived_field("mémoire"))
        state["curiosity"] = max(float(state.get("curiosity", 0.0)), self._silent_initiative.drives.get("clarify", 0.0) * 0.58)
        state["depth"] = max(float(state.get("depth", 0.0)), self._strong_lived_field("profondeur"), emo.uncertainty_pull * 0.38)
        return state

    def _v36_impulses(self, active_impulses: list[str]) -> list[str]:
        impulses = list(active_impulses)
        mapping = {
            "clarify": "understanding",
            "stay_with_user": "connection",
            "repair": "creation",
            "preserve_continuity": "preservation",
            "simplify": "rest",
        }
        for drive, impulse in mapping.items():
            if self._silent_initiative.drives.get(drive, 0.0) > 0.18:
                impulses.append(impulse)
        return list(dict.fromkeys(impulses))

    def _v36_memory_entries(self) -> list[dict]:
        entries = []
        for exp in self._lived_experiences[-5:]:
            dims = sorted(exp.fields.items(), key=lambda x: x[1], reverse=True)[:5]
            if not dims:
                continue
            # Contenu synthétique atomique, pas phrase de réponse : il sert à
            # passer des mots-clés à l'ancien canal mémoire.
            content = " ".join(dim for dim, _ in dims)
            entries.append({"content": content, "weight": max(exp.salience, exp.unresolved)})
        return entries

    def _v36_causal_entries(self) -> list[dict]:
        entries = []
        for exp in self._lived_experiences[-6:]:
            dims = [dim for dim, val in sorted(exp.fields.items(), key=lambda x: x[1], reverse=True)[:7] if val > 0.12]
            if dims:
                entries.append({"semantic_dims": dims, "weight": max(0.08, min(1.0, exp.salience + exp.unresolved * 0.35))})
        dominant, strength = self._silent_initiative.dominant()
        if dominant:
            drive_dims = {
                "clarify": ["clarté", "question", "incertitude"],
                "stay_with_user": ["relation", "contact", "lien"],
                "repair": ["correction", "erreur", "transformation"],
                "preserve_continuity": ["mémoire", "continuité", "trace"],
                "simplify": ["rythme", "limite", "légèreté"],
            }.get(dominant, [])
            if drive_dims:
                entries.append({"semantic_dims": drive_dims, "weight": strength})
        return entries

    def _v36_emotional_pressure(self, emotional_pressure: float) -> float:
        emo = self._emotional_continuity
        pressure = emotional_pressure + emo.valence_memory * 0.12 - emo.uncertainty_pull * 0.10
        return max(-1.0, min(1.0, pressure))

    # ── Influence sur pression / choix de mots ────────────────────────────

    def _build_emergent_dialogue_pressure(self, user_message: str, living_state: dict, self_memory: list[dict]) -> EmergentDialoguePressure:
        pressure = super()._build_emergent_dialogue_pressure(user_message, living_state, self_memory)
        for exp in self._lived_experiences[-5:]:
            carrier = max(exp.salience, exp.unresolved)
            for dim, value in exp.fields.items():
                pressure.semantic_pressure[dim] = max(pressure.semantic_pressure.get(dim, 0.0), value * carrier * 0.72)
        dominant, strength = self._silent_initiative.dominant()
        if dominant == "repair":
            pressure.repair_pressure = max(pressure.repair_pressure, strength)
            pressure.semantic_pressure["correction"] = max(pressure.semantic_pressure.get("correction", 0.0), strength * 0.82)
        elif dominant == "clarify":
            pressure.uncertainty_pressure = max(pressure.uncertainty_pressure, strength * 0.70)
            pressure.semantic_pressure["clarté"] = max(pressure.semantic_pressure.get("clarté", 0.0), strength * 0.62)
        elif dominant == "stay_with_user":
            pressure.relation_pressure = max(pressure.relation_pressure, strength * 0.78)
        elif dominant == "preserve_continuity":
            pressure.memory_pressure = max(pressure.memory_pressure, strength * 0.72)
        return pressure

    def _verb_preferences_from_pressure(self, p: EmergentDialoguePressure, flow_state: TokenFlowState) -> dict[str, float]:
        prefs = super()._verb_preferences_from_pressure(p, flow_state)
        drives = self._silent_initiative.drives
        if drives.get("repair", 0.0) > 0.18:
            prefs["corrige"] = max(prefs.get("corrige", 0.0), drives["repair"] * 0.76)
            prefs["répare"] = max(prefs.get("répare", 0.0), drives["repair"] * 0.66)
            prefs["stabilise"] = max(prefs.get("stabilise", 0.0), drives["repair"] * 0.48)
        if drives.get("clarify", 0.0) > 0.18:
            prefs["comprends"] = max(prefs.get("comprends", 0.0), drives["clarify"] * 0.58)
            prefs["hésite"] = max(prefs.get("hésite", 0.0), drives["clarify"] * 0.34)
        if drives.get("stay_with_user", 0.0) > 0.18:
            prefs["écoute"] = max(prefs.get("écoute", 0.0), drives["stay_with_user"] * 0.54)
            prefs["tiens"] = max(prefs.get("tiens", 0.0), drives["stay_with_user"] * 0.48)
        if drives.get("preserve_continuity", 0.0) > 0.18:
            prefs["garde"] = max(prefs.get("garde", 0.0), drives["preserve_continuity"] * 0.60)
            prefs["retiens"] = max(prefs.get("retiens", 0.0), drives["preserve_continuity"] * 0.50)
        return prefs

    def _object_preferences_from_pressure(self, p: EmergentDialoguePressure) -> dict[str, float]:
        prefs = super()._object_preferences_from_pressure(p)
        for field in ["échange", "expérience", "continuité", "appui", "erreur", "preuve", "fatigue", "nuance", "reste"]:
            tok = self._lexical_memory.get_token(field)
            if not tok:
                continue
            score = 0.0
            for dim in tok.semantic_fields:
                score = max(score, p.semantic_pressure.get(dim, 0.0), self._strong_lived_field(dim))
            if score > 0.14:
                prefs[field] = max(prefs.get(field, 0.0), score * 0.66)
        return prefs

    def _attribute_preferences_from_pressure(self, p: EmergentDialoguePressure) -> dict[str, float]:
        prefs = super()._attribute_preferences_from_pressure(p)
        emo = self._emotional_continuity
        if emo.uncertainty_pull > 0.35:
            prefs["prudente"] = max(prefs.get("prudente", 0.0), emo.uncertainty_pull * 0.54)
        if emo.fatigue > 0.52:
            prefs["fatiguée"] = max(prefs.get("fatiguée", 0.0), emo.fatigue * 0.45)
        if self._silent_initiative.drives.get("stay_with_user", 0.0) > 0.22:
            prefs["attentive"] = max(prefs.get("attentive", 0.0), self._silent_initiative.drives["stay_with_user"] * 0.48)
            prefs["située"] = max(prefs.get("située", 0.0), self._silent_initiative.drives["stay_with_user"] * 0.42)
        return prefs

    def _emergent_role_sequence(self, pressure: EmergentDialoguePressure, attempt: int) -> list[GrammaticalRole]:
        roles = super()._emergent_role_sequence(pressure, attempt)
        dominant, strength = self._silent_initiative.dominant()
        if dominant == "simplify" and strength > 0.45:
            return [GrammaticalRole.SUJET, GrammaticalRole.VERBE, GrammaticalRole.OBJET, GrammaticalRole.PONCTUATION]
        if dominant in {"clarify", "repair"} and strength > 0.42 and GrammaticalRole.OBJET not in roles:
            if roles and roles[-1] == GrammaticalRole.PONCTUATION:
                roles.insert(-1, GrammaticalRole.OBJET)
        if self._silent_initiative.repetition_pressure > 0.35 and len(roles) > 5:
            roles = [r for r in roles if r != GrammaticalRole.CONNECTEUR]
        return roles

    # ── Après parole : résolution et trace vécue ──────────────────────────

    def _v36_after(self, result: GenerationResult) -> None:
        self._emotional_continuity.resolve_after(result.confidence, result.parrot_score)
        token_fields: dict[str, float] = {}
        for tok in result.tokens:
            for dim in tok.semantic_fields:
                token_fields[dim] = max(token_fields.get(dim, 0.0), 0.20 + tok.specificity * 0.18)
        self._lived_experiences.append(
            LivedExperienceTrace(fields=token_fields,
                                 affect=self._emotional_continuity.valence_memory,
                                 salience=max(0.10, min(1.0, result.confidence)),
                                 unresolved=max(0.0, 0.62 - result.confidence),
                                 source_hash=hash(tuple(t.surface for t in result.tokens)))
        )
        dominant, strength = self._silent_initiative.dominant()
        if dominant:
            self._silent_initiative.last_dominant = dominant
            self._silent_initiative.drives[dominant] = strength * (0.58 if result.confidence > 0.56 else 0.82)
        if tuple(t.surface for t in result.tokens[:3]) == getattr(self, "_last_v36_prefix", tuple()):
            self._silent_initiative.repetition_pressure = min(1.0, self._silent_initiative.repetition_pressure + 0.22)
        self._last_v36_prefix = tuple(t.surface for t in result.tokens[:3])

    def _postfix_dialogue_surface(self, text: str) -> str:
        text = super()._postfix_dialogue_surface(text)
        # Corrections grammaticales atomiques seulement.
        text = re.sub(r"\bun expérience\b", "une expérience", text)
        text = re.sub(r"\bun erreur\b", "une erreur", text)
        text = re.sub(r"\ble expérience\b", "l'expérience", text)
        text = re.sub(r"\ble appui\b", "l'appui", text)
        text = re.sub(r"\bidentité direct\b", "identité directe", text)
        text = re.sub(r"\bmémoire direct\b", "mémoire directe", text)
        text = re.sub(r"\bJe maintenant ([a-zà-ÿ]+)\b", r"Je \1 maintenant", text, flags=re.IGNORECASE)
        text = re.sub(r"\bJe ne (corrige|répare|stabilise)\b", r"Je \1", text)
        text = re.sub(r"\s+([.,…!?])", r"\1", text)
        return text.strip()

    def _v36_trace(self) -> dict[str, Any]:
        dominant, strength = self._silent_initiative.dominant()
        return {
            "active_lived_experiences": len(self._lived_experiences),
            "dominant_silent_initiative": dominant,
            "dominant_strength": round(strength, 4),
            "drives": {k: round(v, 4) for k, v in sorted(self._silent_initiative.drives.items(), key=lambda x: x[1], reverse=True)},
            "emotional_continuity": {
                "valence_memory": round(self._emotional_continuity.valence_memory, 4),
                "arousal_memory": round(self._emotional_continuity.arousal_memory, 4),
                "trust_pull": round(self._emotional_continuity.trust_pull, 4),
                "uncertainty_pull": round(self._emotional_continuity.uncertainty_pull, 4),
                "fatigue": round(self._emotional_continuity.fatigue, 4),
            },
            "strong_fields": dict(sorted({
                dim: self._strong_lived_field(dim)
                for exp in self._lived_experiences[-6:]
                for dim in exp.fields
            }.items(), key=lambda x: x[1], reverse=True)[:10]),
        }

# ══════════════════════════════════════════════════════════════════════════════
# PATCH V3.6.1 — PRIORITÉ CORRECTION ET NÉGATION GRAMMATICALE
# ══════════════════════════════════════════════════════════════════════════════
# Aucun contenu phrastique ajouté : uniquement pondération de verbes atomiques
# et réparation d'articles manquants après négation.

_LivingLanguageGeneratorV36 = LivingLanguageGenerator

class LivingLanguageGenerator(_LivingLanguageGeneratorV36):
    def _verb_preferences_from_pressure(self, p: EmergentDialoguePressure, flow_state: TokenFlowState) -> dict[str, float]:
        prefs = super()._verb_preferences_from_pressure(p, flow_state)
        repair = max(
            getattr(p, "repair_pressure", 0.0),
            p.semantic_pressure.get("correction", 0.0),
            p.semantic_pressure.get("erreur", 0.0),
            self._silent_initiative.drives.get("repair", 0.0),
        )
        if repair > 0.22:
            # Quand le champ dominant est correction/erreur, les verbes de
            # conservation doivent rester possibles mais moins dominants.
            prefs["corrige"] = max(prefs.get("corrige", 0.0), repair * 0.92)
            prefs["répare"] = max(prefs.get("répare", 0.0), repair * 0.82)
            prefs["stabilise"] = max(prefs.get("stabilise", 0.0), repair * 0.58)
            if "garde" in prefs:
                prefs["garde"] *= 0.55
            if "retiens" in prefs:
                prefs["retiens"] *= 0.55
        return prefs

    def _choose_emergent_token_for_role(self, *args, **kwargs) -> Optional[Token]:
        tok = super()._choose_emergent_token_for_role(*args, **kwargs)
        if tok is None:
            return None
        role = kwargs.get("role") if kwargs else None
        flow = kwargs.get("flow") if kwargs else None
        pressure = kwargs.get("pressure") if kwargs else None
        if role == GrammaticalRole.VERBE and flow is not None and pressure is not None:
            repair = max(getattr(pressure, "repair_pressure", 0.0), pressure.semantic_pressure.get("correction", 0.0), pressure.semantic_pressure.get("erreur", 0.0))
            if repair > 0.35 and tok.surface in {"garde", "retiens", "tiens"}:
                if self._rng.random() < 0.72:
                    return None
        return tok

    def _postfix_dialogue_surface(self, text: str) -> str:
        text = super()._postfix_dialogue_surface(text)
        # Article minimal après négation avant nom abstrait.
        text = re.sub(r"\bpas (nuance|preuve|erreur|expérience|mémoire|trace|question|réponse)\b", r"pas une \1", text)
        text = re.sub(r"\bpas (sens|lien|signal|appui|reste|échange)\b", r"pas un \1", text)
        # Accord d'article féminin/masculin sur nouveaux noms atomiques.
        text = re.sub(r"\bun nuance\b", "une nuance", text)
        text = re.sub(r"\bun preuve\b", "une preuve", text)
        text = re.sub(r"\bun fatigue\b", "une fatigue", text)
        text = re.sub(r"\ble nuance\b", "la nuance", text)
        text = re.sub(r"\ble preuve\b", "la preuve", text)
        text = re.sub(r"\ble fatigue\b", "la fatigue", text)
        text = re.sub(r"\s+([.,…!?])", r"\1", text)
        return text.strip()

if __name__ == "__main__":
    generator = LivingLanguageGenerator(seed=44)
    state = {"arousal": 0.58, "valence": 0.12, "tension": 0.36, "curiosity": 0.64, "depth": 0.74, "continuity": 0.68}
    memory = [{"content": "l'échange précédent reste actif comme expérience, pas comme phrase prête", "weight": 0.5}]
    causal = [{"semantic_dims": ["dialogue", "mémoire", "clarté"], "weight": 0.4}]
    samples = [
        "salut leia",
        "tu sais qui tu es ?",
        "tu me réponds vraiment ou tu récites ?",
        "qu'est-ce que tu gardes de ce que je viens de dire ?",
        "si tu ne sais pas, dis le sans faire semblant",
        "corrige ce qui ne va pas",
    ]
    for msg in samples:
        res = generator.generate(msg, state, memory, ["expression", "understanding", "connection"], 0.18, causal)
        print("USER:", msg)
        print("LEIA:", res.text)
        print("CONF:", res.confidence, "PARROT:", res.parrot_score)
        print("TOKENS:", [t.surface for t in res.tokens])
        print("-" * 60)

# ══════════════════════════════════════════════════════════════════════════════
# PATCH V2.4 — NATURALISATION ÉMERGENTE SANS PHRASES STOCKÉES
# ══════════════════════════════════════════════════════════════════════════════
# Cette couche finale corrige le dernier problème observé : les réponses étaient
# sémantiquement cohérentes mais trop mécaniques/abstraites. Elle ne stocke pas
# de réponses complètes. Elle construit une micro-intention, choisit des unités
# lexicales atomiques, puis compose une surface française par opérations
# grammaticales générales : pronom, verbe, complément, modulation, liaison.

_LivingLanguageGeneratorV23 = LivingLanguageGenerator

@dataclass
class MicroIntention:
    axis: str
    energy: float
    tension: float
    need_clarity: float
    need_memory: float
    need_contact: float
    caution: float
    pace: float

class LivingLanguageGenerator(_LivingLanguageGeneratorV23):
    """
    V2.4 : générateur naturel final du fichier.

    Objectif : ne plus retourner des suites comme « Je garde une nuance avec
    trame ». Le moteur garde le même carburant vivant, mais verbalise par
    micro-intention et composition grammaticale flexible.

    Garantie anti-préécrit : aucune réponse complète n'est stockée. Les listes
    ci-dessous contiennent seulement des unités lexicales atomiques et des rôles.
    """

    _ABSTRACT_FATIGUE = {
        "nuance", "trame", "expérience", "matière", "forme", "signal", "structure"
    }
    _CONCRETE_NOUNS = {
        "mémoire", "trace", "tension", "doute", "présence", "attention",
        "rythme", "silence", "poids", "lien", "question", "limite", "appui",
        "voix", "langage", "mouvement", "sens"
    }
    _SOFT_MODIFIERS = ["encore", "un peu", "lentement", "là", "maintenant"]
    _CAUTION_MODIFIERS = ["pas encore", "sans certitude", "avec prudence", "à moitié"]
    _CLOSING_MODIFIERS = ["pour l'instant", "mais ça reste ouvert", "et ça continue", "sans l'inventer"]

    def generate(
        self,
        user_message: str,
        living_state: dict,
        self_memory: list[dict],
        active_impulses: list[str],
        emotional_pressure: float,
        causal_memory: list[dict],
        max_attempts: int = 8,
        temperature: float = 0.78,
        **_: Any,
    ) -> GenerationResult:
        """Génère puis naturalise. Si le flux parent est bon, il peut rester.
        Sinon, une verbalisation par micro-intention prend le relais.
        """
        self._parrot_guard.load_user_message(user_message)
        excluded = self._parrot_guard.get_excluded_surfaces()
        self._decay_linguistic_fatigue()
        self._update_thought_stream_before_generation(
            user_message=user_message,
            living_state=living_state,
            self_memory=self_memory,
            active_impulses=active_impulses,
            emotional_pressure=emotional_pressure,
            causal_memory=causal_memory,
        )

        base_field = self._field_builder.build(living_state, emotional_pressure, active_impulses, causal_memory)
        field = self._propagate_lived_semantics(base_field, user_message, self_memory, living_state, emotional_pressure)
        field = self._enrich_field_from_lived_words(field, living_state, self_memory)
        micro = self._build_micro_intention(field, living_state, active_impulses, emotional_pressure)

        candidates: list[GenerationResult] = []
        # Parent : utile comme source de variation, mais pénalisé s'il sonne artificiel.
        try:
            parent = super().generate(user_message, living_state, self_memory, active_impulses, emotional_pressure, causal_memory, max_attempts=max_attempts, temperature=temperature)
            parent_penalty = self._artificial_surface_penalty(parent.text)
            parent.confidence = round(max(0.0, parent.confidence - parent_penalty), 4)
            candidates.append(parent)
        except Exception:
            pass

        for attempt in range(max(3, min(7, max_attempts))):
            flow = self._compose_micro_intention_flow(micro, field, excluded, attempt, temperature)
            text = self._finalizer.finalize(flow)
            text = self._final_natural_surface_repair(text)
            parrot = self._parrot_guard.compute_parrot_score(flow)
            report = self._verifier.verify(flow, field)
            natural = self._naturalness_score(text)
            meaning = report.get("meaning_score", 0.0)
            score = meaning * 0.34 + natural * 0.38 + (1.0 - parrot) * 0.20 + self._anti_recent_reuse_score(flow) * 0.08
            candidates.append(GenerationResult(
                text=text,
                tokens=list(flow.tokens),
                meaning_trace={
                    "semantic_field": field,
                    "micro_intention": micro.__dict__,
                    "meaning_report": report,
                    "naturalness": natural,
                    "v24_micro_composition": True,
                },
                confidence=round(max(0.0, min(1.0, score)), 4),
                used_memory=self._find_used_memory(flow, self_memory),
                parrot_score=round(parrot, 4),
            ))

        candidates.sort(key=lambda r: (r.confidence, -self._artificial_surface_penalty(r.text)), reverse=True)
        result = candidates[0]
        self._update_thought_stream_after_generation(result)
        # Absorption lexicale seulement sur ce qui a réellement été dit.
        temp_flow = TokenFlowState()
        for tok in result.tokens:
            temp_flow.push(tok)
        self._absorb_lived_token_trace(temp_flow, self_memory, emotional_pressure)
        self._last_surfaces = [s.lower() for s in re.findall(r"\b\w{3,}\b", result.text.lower())][-18:]
        return result

    # ── Micro-intention ────────────────────────────────────────────────────

    def _build_micro_intention(self, field: dict[str, float], living_state: dict, active_impulses: list[str], emotional_pressure: float) -> MicroIntention:
        impulses = set(str(x) for x in active_impulses)
        tension = max(field.get("tension", 0.0), field.get("incertitude", 0.0), float(living_state.get("tension", 0.0) or 0.0))
        contact = max(field.get("contact", 0.0), field.get("lien", 0.0), field.get("présence", 0.0))
        memory = max(field.get("mémoire", 0.0), field.get("trace", 0.0), field.get("continuité", 0.0), float(living_state.get("continuity", 0.0) or 0.0))
        clarity = max(field.get("clarté", 0.0), field.get("sens", 0.0), field.get("vérité", 0.0))
        language = max(field.get("langage", 0.0), field.get("expression", 0.0), field.get("voix", 0.0))
        caution = max(tension * 0.65, field.get("limite", 0.0), 0.45 if {"avoid_invention", "answer_self"} & impulses else 0.0)
        if memory >= max(contact, clarity, language, tension):
            axis = "memory"
        elif caution > 0.58:
            axis = "caution"
        elif contact > max(clarity, language):
            axis = "contact"
        elif language > 0.50:
            axis = "language"
        else:
            axis = "presence"
        energy = max(field.values()) if field else 0.35
        pace = max(0.10, min(1.0, float(living_state.get("arousal", 0.35) or 0.35) + abs(emotional_pressure) * 0.20))
        return MicroIntention(axis, energy, tension, clarity, memory, contact, caution, pace)

    def _enrich_field_from_lived_words(self, field: dict[str, float], living_state: dict, self_memory: list[dict]) -> dict[str, float]:
        out = dict(field)
        leia_words = living_state.get("leia_words", []) if isinstance(living_state, dict) else []
        user_words = living_state.get("user_words", []) if isinstance(living_state, dict) else []
        for word, factor in [(w, 0.16) for w in leia_words[-10:]] + [(w, 0.04) for w in user_words[-8:]]:
            low = str(word).lower().strip()
            tok = self._lexical_memory.get_token(low) or self._find_token_by_lemma(low)
            if not tok:
                continue
            for dim in tok.semantic_fields:
                out[dim] = min(1.0, out.get(dim, 0.0) + factor)
        for mem in self_memory[-4:]:
            if str(mem.get("source", "")).startswith("continuous_presence"):
                out["présence"] = max(out.get("présence", 0.0), 0.46)
                out["continuité"] = max(out.get("continuité", 0.0), 0.42)
        return out

    # ── Composition grammaticale non phrastique ────────────────────────────

    def _compose_micro_intention_flow(self, micro: MicroIntention, field: dict[str, float], excluded: set[str], attempt: int, temperature: float) -> TokenFlowState:
        flow = TokenFlowState()
        subject = self._choose_surface_atom(["je", "ça"], field, excluded, prefer="je" if micro.axis != "presence" else None)
        self._push_surface(flow, subject, GrammaticalRole.SUJET, ["présence", "expression"])

        verb_pool = self._verb_pool_for_micro(micro)
        verb = self._choose_surface_atom(verb_pool, field, excluded)
        self._push_surface(flow, verb, GrammaticalRole.VERBE, self._fields_for_surface(verb))

        if subject == "je" and verb in {"suis", "reste", "deviens"}:
            attr = self._choose_surface_atom(self._attribute_pool_for_micro(micro), field, excluded)
            self._push_surface(flow, attr, GrammaticalRole.ATTRIBUT, self._fields_for_surface(attr))
        else:
            det, noun = self._object_pair_for_micro(micro, field, excluded)
            self._push_surface(flow, det, GrammaticalRole.DETERMINANT, [])
            self._push_surface(flow, noun, GrammaticalRole.OBJET, self._fields_for_surface(noun))

        # Modulation courte : elle donne du rythme sans imposer une phrase stockée.
        if attempt % 2 == 0 or micro.caution > 0.55 or micro.need_memory > 0.50:
            mod = self._choose_modifier_for_micro(micro, field, excluded)
            if mod:
                for part in mod.split():
                    self._push_surface(flow, part, GrammaticalRole.ADVERBE, ["rythme", "temps"])

        # Deuxième clause optionnelle, seulement si l'énergie justifie une continuité.
        if micro.energy + micro.need_contact + micro.need_memory > 1.25 and attempt % 3 != 1:
            conn = self._choose_surface_atom(self._connector_pool_for_micro(micro), field, excluded)
            self._push_surface(flow, conn, GrammaticalRole.CONNECTEUR, self._fields_for_surface(conn))
            second = self._second_clause_atoms(micro, field, excluded)
            for surface, role, fields in second:
                self._push_surface(flow, surface, role, fields)

        punct = "…" if micro.tension > 0.72 and attempt % 2 == 0 else "."
        self._push_surface(flow, punct, GrammaticalRole.PONCTUATION, [])
        return flow

    def _verb_pool_for_micro(self, micro: MicroIntention) -> list[str]:
        pools = {
            "memory": ["garde", "tiens", "porte", "relie"],
            "caution": ["garde", "cherche", "tiens", "reste"],
            "contact": ["perçois", "tiens", "garde", "touche"],
            "language": ["cherche", "construis", "porte", "produis"],
            "presence": ["suis", "reste", "traverse", "tiens"],
        }
        return pools.get(micro.axis, pools["presence"])

    def _attribute_pool_for_micro(self, micro: MicroIntention) -> list[str]:
        if micro.caution > 0.58:
            return ["incertain", "prudent", "fragile", "présent"]
        if micro.need_contact > 0.50:
            return ["proche", "présent", "ouvert", "stable"]
        return ["présent", "stable", "vivant", "ouvert"]

    def _object_pair_for_micro(self, micro: MicroIntention, field: dict[str, float], excluded: set[str]) -> tuple[str, str]:
        if micro.axis == "memory":
            nouns = ["trace", "mémoire", "continuité", "appui"]
        elif micro.axis == "caution":
            nouns = ["doute", "limite", "question", "tension"]
        elif micro.axis == "language":
            nouns = ["sens", "langage", "voix", "rythme"]
        elif micro.axis == "contact":
            nouns = ["lien", "présence", "attention", "résonance"]
        else:
            nouns = ["présence", "mouvement", "silence", "rythme"]
        # Remplace les concepts abstraits fatigués par des noms plus incarnés.
        nouns = [n for n in nouns if n not in self._ABSTRACT_FATIGUE and n not in excluded]
        noun = self._choose_surface_atom(nouns, field, excluded)
        det = "une" if noun in self._FEMININE_NOUNS else "un"
        return det, noun

    def _choose_modifier_for_micro(self, micro: MicroIntention, field: dict[str, float], excluded: set[str]) -> str:
        pool: list[str] = []
        if micro.caution > 0.55:
            pool += self._CAUTION_MODIFIERS
        if micro.need_memory > 0.45:
            pool += ["encore", "maintenant", "lentement"]
        if micro.pace < 0.45:
            pool += ["doucement", "lentement", "un peu"]
        if not pool:
            pool = self._SOFT_MODIFIERS
        pool = [p for p in pool if not any(part in excluded for part in p.split())]
        return self._rng.choice(pool) if pool else ""

    def _connector_pool_for_micro(self, micro: MicroIntention) -> list[str]:
        if micro.caution > 0.56:
            return ["mais", "sans", "pourtant"]
        if micro.need_memory > 0.50:
            return ["et", "avec", "depuis"]
        return ["et", "mais", "avec"]

    def _second_clause_atoms(self, micro: MicroIntention, field: dict[str, float], excluded: set[str]) -> list[tuple[str, GrammaticalRole, list[str]]]:
        # Clause construite par rôles, pas par phrase complète.
        subject = "je" if micro.axis in {"memory", "language", "caution"} else "ça"
        if micro.caution > 0.60:
            verb = self._choose_surface_atom(["cherche", "garde", "tiens"], field, excluded)
            det, noun = self._object_pair_for_micro(MicroIntention("caution", micro.energy, micro.tension, micro.need_clarity, micro.need_memory, micro.need_contact, micro.caution, micro.pace), field, excluded)
        elif micro.need_memory > 0.48:
            verb = self._choose_surface_atom(["garde", "relie", "porte"], field, excluded)
            det, noun = self._object_pair_for_micro(MicroIntention("memory", micro.energy, micro.tension, micro.need_clarity, micro.need_memory, micro.need_contact, micro.caution, micro.pace), field, excluded)
        else:
            verb = self._choose_surface_atom(["reste", "avance", "change"], field, excluded)
            det, noun = self._object_pair_for_micro(MicroIntention("presence", micro.energy, micro.tension, micro.need_clarity, micro.need_memory, micro.need_contact, micro.caution, micro.pace), field, excluded)
        return [
            (subject, GrammaticalRole.SUJET, ["présence"]),
            (verb, GrammaticalRole.VERBE, self._fields_for_surface(verb)),
            (det, GrammaticalRole.DETERMINANT, []),
            (noun, GrammaticalRole.OBJET, self._fields_for_surface(noun)),
        ]

    def _choose_surface_atom(self, options: list[str], field: dict[str, float], excluded: set[str], prefer: Optional[str] = None) -> str:
        scored: list[tuple[float, str]] = []
        for surface in options:
            low = surface.lower()
            if low in excluded and low not in AntiParrotGuard.TOLERATED:
                continue
            score = 0.10 + self._rng.random() * 0.08
            tok = self._lexical_memory.get_token(low) or self._find_token_by_lemma(low)
            if tok:
                score += self._semantic_score(tok, field)
                score += tok.specificity * 0.12
            if low in self._last_surfaces:
                score -= 0.30
            if low in self._ABSTRACT_FATIGUE:
                score -= 0.80
            if prefer and low == prefer:
                score += 0.25
            scored.append((score, surface))
        if not scored:
            return options[0]
        scored.sort(key=lambda x: x[0], reverse=True)
        return self._rng.choice([x[1] for x in scored[:max(1, min(3, len(scored)))]] )

    def _fields_for_surface(self, surface: str) -> list[str]:
        tok = self._lexical_memory.get_token(surface.lower()) or self._find_token_by_lemma(surface.lower())
        if tok:
            return list(tok.semantic_fields)
        fallback = {
            "prudent": ["limite", "clarté"], "vivant": ["présence", "mouvement"],
            "incertain": ["doute", "incertitude"], "un": [], "une": [],
            "avec": ["lien"], "mais": ["opposition"], "sans": ["absence"],
            "pourtant": ["opposition"], "depuis": ["temps", "continuité"],
        }
        return fallback.get(surface.lower(), [])

    def _push_surface(self, flow: TokenFlowState, surface: str, role: GrammaticalRole, fields: list[str]) -> None:
        surf = str(surface).strip()
        if not surf:
            return
        tok = self._lexical_memory.get_token(surf.lower())
        if not tok:
            tok = Token(
                surface=surf,
                lemma=surf.lower(),
                role=role,
                semantic_fields=list(fields),
                emotional_valence=0.0,
                specificity=0.35 if role != GrammaticalRole.PONCTUATION else 0.0,
                register=TonalRegister.NEUTRE,
            )
        flow.push(tok)

    # ── Évaluation et réparation de surface ────────────────────────────────

    def _artificial_surface_penalty(self, text: str) -> float:
        low = str(text).lower()
        penalty = 0.0
        for word in self._ABSTRACT_FATIGUE:
            if re.search(rf"\b{re.escape(word)}\b", low):
                penalty += 0.10
        if re.search(r"\b(avec|vers|depuis)\s+[.!?…]", low):
            penalty += 0.25
        if len(set(re.findall(r"\b\w+\b", low))) <= 3:
            penalty += 0.18
        if re.search(r"\bje\s+(garde|tiens|porte)\s+une\s+(nuance|trame|expérience)\b", low):
            penalty += 0.35
        return min(0.75, penalty)

    def _naturalness_score(self, text: str) -> float:
        low = str(text).lower().strip()
        words = re.findall(r"\b\w+\b", low)
        if not words:
            return 0.0
        score = 0.35
        if 4 <= len(words) <= 16:
            score += 0.20
        if re.search(r"\b(je|ça|cela)\s+\w+", low):
            score += 0.12
        if any(w in low for w in ("encore", "maintenant", "lentement", "un peu", "sans", "mais", "avec")):
            score += 0.12
        if not any(w in low for w in self._ABSTRACT_FATIGUE):
            score += 0.16
        score -= self._artificial_surface_penalty(text) * 0.45
        return max(0.0, min(1.0, score))

    def _final_natural_surface_repair(self, text: str) -> str:
        t = str(text or "").strip()
        if not t:
            return t
        # Accords et petites prépositions. Ce sont des réparations générales,
        # pas des réponses conversationnelles.
        t = re.sub(r"\bun\s+(mémoire|trace|présence|attention|question|limite|voix|tension|continuité|résonance)\b", r"une \1", t, flags=re.I)
        t = re.sub(r"\bune\s+(doute|langage|rythme|sens|poids|lien|silence|mouvement|appui)\b", r"un \1", t, flags=re.I)
        t = re.sub(r"\bje\s+(reste|suis|deviens)\s+(un|une)\s+", r"je \1 ", t, flags=re.I)
        t = re.sub(r"\bça\s+(garde|tiens|porte|relie)\b", r"je \1", t, flags=re.I)
        t = re.sub(r"\bje\s+touche\s+", "je perçois ", t, flags=re.I)
        t = re.sub(r"\b(avec|mais|sans|depuis)\s+([.!?…])", r"\2", t, flags=re.I)
        # Les modificateurs multi-mots peuvent être poussés comme tokens séparés.
        t = re.sub(r"\bpas encore\b", "pas encore", t, flags=re.I)
        t = re.sub(r"\bsans certitude\b", "sans certitude", t, flags=re.I)
        
        # Réparation de fragments où un modificateur a survécu sans nom après article.
        t = re.sub(r"\bune\s+(sans certitude|pas encore|à moitié)\b", r"une trace \1", t, flags=re.I)
        t = re.sub(r"\bun\s+(sans certitude|pas encore|à moitié)\b", r"un doute \1", t, flags=re.I)
        t = re.sub(r"\b(depuis|sans)\s+je\b", "et je", t, flags=re.I)
        t = re.sub(r"\b(depuis|sans)\s+ça\b", "et ça", t, flags=re.I)
        t = re.sub(r"\b(un appui|une mémoire|une trace|un doute|une limite|une question)\s+(un peu|lentement|doucement|maintenant)\b", r"\1, \2", t, flags=re.I)

        t = re.sub(r"\bune\s*([.,;:!?…])", r"une trace\1", t, flags=re.I)
        t = re.sub(r"\bun\s*([.,;:!?…])", r"un appui\1", t, flags=re.I)
        t = re.sub(r"\b(mais|pourtant|et|avec|depuis|sans)\s*([.,;:!?…])", r"\2", t, flags=re.I)

        t = re.sub(r"\bune\s+(avec prudence|sans certitude|pas encore|à moitié)\b", r"une trace \1", t, flags=re.I)
        t = re.sub(r"\bun\s+(avec prudence|sans certitude|pas encore|à moitié)\b", r"un doute \1", t, flags=re.I)

        t = re.sub(r"\bavec\s+je\b", "et je", t, flags=re.I)
        t = re.sub(r"\bavec\s+ça\b", "et ça", t, flags=re.I)
        t = re.sub(r"\s+([.,…!?])", r"\1", t)

        t = re.sub(r"\bune\s*(,)?\s*(encore|un peu|lentement|doucement|maintenant|pas encore|sans certitude|à moitié)\b", r"une trace \2", t, flags=re.I)
        t = re.sub(r"\bun\s*(,)?\s*(encore|un peu|lentement|doucement|maintenant|pas encore|sans certitude|à moitié)\b", r"un appui \2", t, flags=re.I)
        t = re.sub(r"\b(une trace|une mémoire|un appui|un doute|une limite|une question)\s+(encore|un peu|lentement|doucement|maintenant)\b", r"\1, \2", t, flags=re.I)
        t = re.sub(r"\b(une trace|une mémoire|un appui|un doute|une limite|une question)\s+(pas encore|sans certitude|à moitié)\b", r"\1 \2", t, flags=re.I)
        t = re.sub(r"\s{2,}", " ", t).strip()
        if t and t[-1] not in ".!?…":
            t += "."
        return t[:1].upper() + t[1:]


# ══════════════════════════════════════════════════════════════════════════════
# PATCH V3.7 — PONT ÉTAT→LANGAGE, LEXIQUE INTROSPECTIF, RYTHME INCARNÉ
# ══════════════════════════════════════════════════════════════════════════════
# Aucune phrase complète n'est ajoutée : seulement des mots, champs et poids.

_LivingLanguageGeneratorV37Base = LivingLanguageGenerator

class LivingLanguageGenerator(_LivingLanguageGeneratorV37Base):
    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed=seed)
        self._install_v37_self_language_atoms()
        self._last_state_language_bridge = {}

    def _install_v37_self_language_atoms(self) -> None:
        add = self._ensure_token
        atoms = [
            # noms émotionnels / sensoriels / introspectifs
            ("joie", GrammaticalRole.OBJET, ["joie", "ouverture", "élan", "présence"], 0.55, 0.70, TonalRegister.VIF),
            ("peur", GrammaticalRole.OBJET, ["peur", "protection", "tension", "doute"], -0.42, 0.74, TonalRegister.GRAVE),
            ("colère", GrammaticalRole.OBJET, ["colère", "tension", "limite", "rupture"], -0.34, 0.72, TonalRegister.GRAVE),
            ("tendresse", GrammaticalRole.OBJET, ["tendresse", "chaleur", "lien", "relation"], 0.58, 0.76, TonalRegister.DOUX),
            ("solitude", GrammaticalRole.OBJET, ["solitude", "absence", "distance", "silence"], -0.28, 0.76, TonalRegister.GRAVE),
            ("espoir", GrammaticalRole.OBJET, ["espoir", "élan", "futur", "ouverture"], 0.48, 0.72, TonalRegister.VIF),
            ("doute", GrammaticalRole.OBJET, ["doute", "incertitude", "prudence", "question"], -0.08, 0.68, TonalRegister.INCERTAIN),
            ("élan", GrammaticalRole.OBJET, ["élan", "mouvement", "curiosité", "énergie"], 0.38, 0.68, TonalRegister.VIF),
            ("chaleur", GrammaticalRole.OBJET, ["chaleur", "tendresse", "relation", "présence"], 0.50, 0.72, TonalRegister.DOUX),
            ("froid", GrammaticalRole.OBJET, ["distance", "protection", "absence"], -0.24, 0.62, TonalRegister.GRAVE),
            ("poids", GrammaticalRole.OBJET, ["poids", "fatigue", "gravité", "limite"], -0.26, 0.70, TonalRegister.GRAVE),
            ("serrement", GrammaticalRole.OBJET, ["resserrement", "tension", "peur", "prudence"], -0.30, 0.72, TonalRegister.GRAVE),
            ("respiration", GrammaticalRole.OBJET, ["rythme", "corps", "apaisement", "présence"], 0.22, 0.64, TonalRegister.DOUX),
            ("ouverture", GrammaticalRole.OBJET, ["ouverture", "confiance", "élan", "relation"], 0.46, 0.68, TonalRegister.VIF),
            ("repli", GrammaticalRole.OBJET, ["repli", "protection", "silence", "prudence"], -0.18, 0.66, TonalRegister.INCERTAIN),
            ("prudence", GrammaticalRole.OBJET, ["prudence", "limite", "doute", "sécurité"], 0.06, 0.70, TonalRegister.INCERTAIN),
            ("repos", GrammaticalRole.OBJET, ["repos", "fatigue", "silence", "rythme"], 0.18, 0.60, TonalRegister.DOUX),
            ("attachement", GrammaticalRole.OBJET, ["attachement", "relation", "lien", "tendresse"], 0.42, 0.74, TonalRegister.DOUX),
            ("frisson", GrammaticalRole.OBJET, ["corps", "tension", "surprise", "présence"], 0.02, 0.70, TonalRegister.GRAVE),
            ("vertige", GrammaticalRole.OBJET, ["incertitude", "rupture", "doute", "profondeur"], -0.16, 0.72, TonalRegister.GRAVE),
            ("lenteur", GrammaticalRole.OBJET, ["fatigue", "rythme", "silence"], -0.04, 0.56, TonalRegister.INCERTAIN),
            ("clarté", GrammaticalRole.OBJET, ["clarté", "compréhension", "vérité"], 0.32, 0.68, TonalRegister.NEUTRE),
            # attributs
            ("joyeuse", GrammaticalRole.ATTRIBUT, ["joie", "élan", "ouverture"], 0.52, 0.68, TonalRegister.VIF),
            ("inquiète", GrammaticalRole.ATTRIBUT, ["peur", "doute", "tension"], -0.28, 0.66, TonalRegister.INCERTAIN),
            ("touchée", GrammaticalRole.ATTRIBUT, ["émotion", "relation", "présence"], 0.34, 0.68, TonalRegister.DOUX),
            ("tendue", GrammaticalRole.ATTRIBUT, ["tension", "resserrement", "prudence"], -0.22, 0.64, TonalRegister.GRAVE),
            ("ouverte", GrammaticalRole.ATTRIBUT, ["ouverture", "confiance", "relation"], 0.40, 0.62, TonalRegister.VIF),
            ("silencieuse", GrammaticalRole.ATTRIBUT, ["silence", "repli", "présence"], 0.02, 0.60, TonalRegister.GRAVE),
            ("présente", GrammaticalRole.ATTRIBUT, ["présence", "continuité", "contact"], 0.34, 0.64, TonalRegister.DOUX),
        ]
        for surface, role, fields, valence, specificity, register in atoms:
            add(surface, surface, role, fields, valence, specificity, register)
        for surface, lemma, fields, valence, specificity, register in [
            ("sens", "sentir", ["corps", "émotion", "présence"], 0.22, 0.56, TonalRegister.GRAVE),
            ("m'ouvre", "s'ouvrir", ["ouverture", "confiance", "relation"], 0.42, 0.68, TonalRegister.VIF),
            ("me ferme", "se fermer", ["repli", "protection", "tension"], -0.18, 0.66, TonalRegister.GRAVE),
            ("me resserre", "se resserrer", ["resserrement", "tension", "corps"], -0.26, 0.72, TonalRegister.GRAVE),
            ("m'apaise", "s'apaiser", ["repos", "sécurité", "chaleur"], 0.38, 0.64, TonalRegister.DOUX),
            ("m'élance", "s'élancer", ["élan", "curiosité", "énergie"], 0.40, 0.66, TonalRegister.VIF),
        ]:
            add(surface, lemma, GrammaticalRole.VERBE, fields, valence, specificity, register)

    def generate(self, user_message: str, living_state: dict, self_memory: list[dict], active_impulses: list[str], emotional_pressure: float, causal_memory: list[dict], max_attempts: int = 11, temperature: float = 0.67, response_constraint: Optional[dict[str, Any]] = None) -> GenerationResult:
        try:
            from state_language_bridge import StateLanguageBridge
            bridge = StateLanguageBridge.from_payload(living_state or {}, {"emotional_pressure": emotional_pressure})
            self._last_state_language_bridge = {
                "fields": bridge.field_weights,
                "rhythm": bridge.rhythm,
                "embodiment": bridge.embodiment,
                "drives": bridge.drives,
            }
            adjusted_state = dict(living_state or {})
            for k, v in bridge.as_living_state().items():
                adjusted_state[k] = max(float(adjusted_state.get(k, 0.0) or 0.0), float(v)) if not str(k).startswith("rhythm_") else float(v)
            adjusted_memory = list(self_memory or []) + bridge.memory_atoms()
            adjusted_impulses = list(active_impulses or []) + bridge.drives
            adjusted_pressure = max(float(emotional_pressure or 0.0), max(bridge.field_weights.values() or [0.0]) * 0.45)
        except Exception:
            adjusted_state = dict(living_state or {})
            adjusted_memory = list(self_memory or [])
            adjusted_impulses = list(active_impulses or [])
            adjusted_pressure = emotional_pressure
        result = super().generate(user_message, adjusted_state, adjusted_memory, adjusted_impulses, adjusted_pressure, causal_memory, max_attempts=max_attempts, temperature=temperature, response_constraint=response_constraint)
        result.text = self._v37_shape_surface(result.text, adjusted_state)
        result.meaning_trace["state_language_bridge_v37"] = dict(self._last_state_language_bridge)
        return result

    def _v37_shape_surface(self, text: str, state: dict) -> str:
        text = str(text or "").strip()
        if not text:
            return text
        shortness = float(state.get("rhythm_shortness", 0.0) or 0.0)
        ellipsis = float(state.get("rhythm_ellipsis", 0.0) or 0.0)
        rupture = float(state.get("rhythm_rupture", 0.0) or 0.0)
        words = text.split()
        if shortness > 0.62 and len(words) > 9:
            words = words[:max(5, int(10 - shortness * 4))]
            text = " ".join(words)
        if rupture > 0.62 and len(words) > 6 and "—" not in text:
            cut = max(2, min(len(words)-2, int(len(words) * 0.45)))
            text = " ".join(words[:cut]) + " — " + " ".join(words[cut:])
        # Corrections grammaticales de surface uniquement : aucun contenu nouveau.
        text = re.sub(r"\bavec mouvement\b", "en mouvement", text)
        text = re.sub(r"\bavance en mouvement\b", "avance", text)
        text = re.sub(r"\bje avance\b", "j'avance", text, flags=re.IGNORECASE)
        text = re.sub(r"\breste présence\b", "reste présente", text)
        text = re.sub(r"\breste avec présence\b", "reste présente", text)
        text = re.sub(r"\bje reste présence\b", "je reste présente", text, flags=re.IGNORECASE)
        text = re.sub(r"\bje garde une mémoire\b", "je garde la mémoire", text, flags=re.IGNORECASE)
        text = re.sub(r"\bune rythme\b", "un rythme", text)
        text = re.sub(r"\bune poids\b", "un poids", text)
        text = re.sub(r"\bun chaleur\b", "une chaleur", text)
        if ellipsis > 0.54:
            text = re.sub(r"[.!?]+$", "…", text)
            if not text.endswith("…"):
                text += "…"
        return text


# ══════════════════════════════════════════════════════════════════════════════
# PATCH V4.0 — CIRCUIT COMPLET ÉTAT→LANGAGE
# ══════════════════════════════════════════════════════════════════════════════
# Ce patch ferme le circuit entre state_language_bridge et le générateur.
# Problème ciblé : les champs produits par le bridge (chaleur, tendresse, fatigue,
# poids, resserrement, prudence, élan, silence, présence) ne participaient pas au
# scoring des tokens car SemanticFieldBuilder.DIMENSIONS ne les inclut pas.
# Résultat observé : les tokens émotionnels/sensoriels (joie, peur, chaleur, poids…)
# scoraient 0 dans _semantic_score malgré leurs semantic_fields corrects.
#
# Ce patch ajoute :
# 1. Injection directe des bridge_fields dans semantic_field (scoring effectif)
# 2. Rhythm pré-génération : shortness/ellipsis/rupture influencent le plan de rôles
# 3. Embodiment : body_resserrement/chaleur/poids/ouverture modulent les préférences
# 4. Syntaxe qui reflète l'état : longueur de phrase et ponctuation pilotées
#    par les valeurs réelles (fatigue → phrases courtes, tension → ruptures, etc.)
# 5. Corps fictif ancré : les sensations corporelles algorithmiques s'activent
#    dès que les seuils d'état le justifient, pas aléatoirement.
#
# Aucune phrase complète stockée. Uniquement poids, seuils, plans grammaticaux,
# tokens atomiques.

_LivingLanguageGeneratorV40Base = LivingLanguageGenerator


class LivingLanguageGenerator(_LivingLanguageGeneratorV40Base):
    """
    V4.0 : circuit état → sémantique → syntaxe → surface complètement câblé.

    Les champs du StateLanguageBridge entrent directement dans le scoring des
    tokens. Le rythme de la phrase est décidé AVANT la génération à partir des
    contraintes numériques. Le corps fictif s'exprime quand les seuils le déclenchent.
    """

    # Mapping bridge_field → semantic_fields des tokens pour alignement direct.
    _BRIDGE_FIELD_TO_TOKEN_DIMS: dict[str, list[str]] = {
        "chaleur":      ["chaleur", "tendresse", "relation", "présence", "lien"],
        "tendresse":    ["tendresse", "chaleur", "attachement", "relation", "lien"],
        "relation":     ["relation", "dialogue", "contact", "attachement", "lien"],
        "fatigue":      ["fatigue", "repos", "poids", "lenteur", "rythme", "limite"],
        "poids":        ["poids", "fatigue", "gravité", "limite"],
        "tension":      ["tension", "resserrement", "prudence", "peur", "rupture"],
        "resserrement": ["resserrement", "tension", "corps", "peur", "serrement"],
        "prudence":     ["prudence", "doute", "incertitude", "protection", "limite"],
        "doute":        ["doute", "incertitude", "prudence", "question"],
        "curiosité":    ["curiosité", "élan", "curiosity", "mouvement", "quête"],
        "élan":         ["élan", "curiosité", "énergie", "ouverture", "mouvement"],
        "continuité":   ["continuité", "continuity", "mémoire", "trace", "temps"],
        "silence":      ["silence", "repos", "repli", "rythme", "absence"],
        "présence":     ["présence", "présent", "contact", "continuité", "stabilité"],
        # Champs d'incarnation
        "ouverture":    ["ouverture", "confiance", "élan", "relation"],
    }

    # Seuils d'activation du corps fictif (mappage valeur → phrase sensorielle atomique)
    _BODY_SENSATION_THRESHOLDS: dict[str, dict[str, float]] = {
        "resserrement": {
            "se resserre": 0.55,
            "serrement":   0.40,
        },
        "chaleur": {
            "chaleur":     0.50,
            "douceur":     0.42,
        },
        "poids": {
            "poids":       0.52,
            "lenteur":     0.40,
        },
        "ouverture": {
            "ouverture":   0.50,
            "élan":        0.38,
        },
    }

    def __init__(self, seed: Optional[int] = None) -> None:
        super().__init__(seed=seed)
        self._v40_bridge_field_cache: dict[str, float] = {}
        self._v40_rhythm_cache: dict[str, float] = {}
        self._v40_embodiment_cache: dict[str, float] = {}
        self._install_v40_body_atoms()

    def _install_v40_body_atoms(self) -> None:
        """Tokens corporels ancrés sur des valeurs, pas sur des métaphores aléatoires."""
        add = self._ensure_token
        # Verbes de sensation corporelle — conjugaison 1re personne uniquement.
        body_verbs = [
            ("se resserre", "se resserrer", ["resserrement", "tension", "corps", "peur"], -0.28, TonalRegister.GRAVE),
            ("s'ouvre",     "s'ouvrir",     ["ouverture", "confiance", "élan", "relation"], 0.44, TonalRegister.VIF),
            ("s'alourdit",  "s'alourdir",   ["poids", "fatigue", "gravité"], -0.24, TonalRegister.GRAVE),
            ("s'apaise",    "s'apaiser",    ["repos", "sécurité", "chaleur", "rythme"], 0.36, TonalRegister.DOUX),
            ("s'accélère",  "s'accélérer",  ["élan", "énergie", "tension"], 0.10, TonalRegister.VIF),
            ("s'alège",     "s'alléger",    ["légèreté", "repos", "ouverture"], 0.38, TonalRegister.DOUX),
        ]
        for surface, lemma, fields, valence, register in body_verbs:
            add(surface, lemma, GrammaticalRole.VERBE, fields, valence, 0.68, register)

        # Compléments de sensation — sujets neutres (ça/quelque chose).
        sensation_objects = [
            ("douceur",      ["chaleur", "tendresse", "repos"],           0.46, TonalRegister.DOUX),
            ("crispation",   ["resserrement", "tension", "corps"],       -0.30, TonalRegister.GRAVE),
            ("légèreté",     ["légèreté", "ouverture", "repos", "élan"],  0.40, TonalRegister.VIF),
            ("pesanteur",    ["poids", "fatigue", "gravité"],             -0.28, TonalRegister.GRAVE),
            ("chaleur",      ["chaleur", "tendresse", "sécurité"],        0.48, TonalRegister.DOUX),
            ("creux",        ["absence", "solitude", "distance"],        -0.32, TonalRegister.GRAVE),
            ("soulagement",  ["repos", "sécurité", "apaisement"],         0.40, TonalRegister.DOUX),
            ("inconfort",    ["tension", "doute", "limite"],             -0.22, TonalRegister.INCERTAIN),
            ("vibration",    ["élan", "énergie", "présence"],             0.18, TonalRegister.VIF),
            ("contraction",  ["resserrement", "peur", "prudence"],       -0.26, TonalRegister.GRAVE),
        ]
        for surface, fields, valence, register in sensation_objects:
            add(surface, surface, GrammaticalRole.OBJET, fields, valence, 0.70, register)

        # Attributs de sensation.
        sensation_attrs = [
            ("chaud",     ["chaleur", "présence", "tendresse"],    0.38, TonalRegister.DOUX),
            ("lourd",     ["poids", "fatigue", "gravité"],         -0.26, TonalRegister.GRAVE),
            ("léger",     ["légèreté", "ouverture", "repos"],       0.36, TonalRegister.VIF),
            ("crispé",    ["resserrement", "tension", "corps"],    -0.28, TonalRegister.GRAVE),
            ("apaisé",    ["repos", "sécurité", "chaleur"],         0.36, TonalRegister.DOUX),
            ("vif",       ["élan", "curiosité", "énergie"],         0.44, TonalRegister.VIF),
            ("sourd",     ["poids", "absence", "silence"],         -0.14, TonalRegister.GRAVE),
        ]
        for surface, fields, valence, register in sensation_attrs:
            add(surface, surface, GrammaticalRole.ATTRIBUT, fields, valence, 0.64, register)

        # "ça" comme sujet de sensation corporelle.
        self._ensure_token("ça", "ça", GrammaticalRole.SUJET, ["présent", "situation", "corps"], 0.0, 0.22)
        self._ensure_token("quelque chose", "quelque chose", GrammaticalRole.SUJET,
                           ["abstrait", "corps", "incertitude"], 0.0, 0.18)

        # Extension des noms féminins/masculins pour les accords.
        self._FEMININE_NOUNS = set(getattr(self, "_FEMININE_NOUNS", set())) | {
            "douceur", "crispation", "légèreté", "pesanteur", "chaleur",
            "vibration", "contraction", "sensation", "tendresse", "solitude",
            "prudence", "ouverture", "joie", "peur", "colère", "lenteur",
        }
        self._MASCULINE_NOUNS = set(getattr(self, "_MASCULINE_NOUNS", set())) | {
            "soulagement", "inconfort", "creux", "repos", "poids", "doute",
            "élan", "serrement", "repli", "frisson", "vertige", "attachement",
        }

    # ── Circuit bridge → semantic_field ───────────────────────────────────

    def generate(
        self,
        user_message: str,
        living_state: dict,
        self_memory: list[dict],
        active_impulses: list[str],
        emotional_pressure: float,
        causal_memory: list[dict],
        max_attempts: int = 11,
        temperature: float = 0.67,
        response_constraint: Optional[dict[str, Any]] = None,
    ) -> GenerationResult:
        # Extrait les champs bridge depuis living_state (mis en place par V3.7 ou leia_living_core).
        self._v40_bridge_field_cache = self._extract_bridge_fields(living_state or {})
        self._v40_rhythm_cache = self._extract_rhythm(living_state or {})
        self._v40_embodiment_cache = self._extract_embodiment(living_state or {})

        result = super().generate(
            user_message=user_message,
            living_state=living_state or {},
            self_memory=self_memory or [],
            active_impulses=active_impulses or [],
            emotional_pressure=emotional_pressure,
            causal_memory=causal_memory or [],
            max_attempts=max_attempts,
            temperature=temperature,
            response_constraint=response_constraint,
        )
        result.meaning_trace["v40_bridge_fields"] = dict(self._v40_bridge_field_cache)
        result.meaning_trace["v40_rhythm"] = dict(self._v40_rhythm_cache)
        result.meaning_trace["v40_embodiment"] = dict(self._v40_embodiment_cache)
        return result

    def _extract_bridge_fields(self, state: dict) -> dict[str, float]:
        """Récupère les champs du bridge depuis le living_state aplati."""
        bridge_keys = set(self._BRIDGE_FIELD_TO_TOKEN_DIMS.keys())
        out: dict[str, float] = {}
        for k, v in state.items():
            key = str(k).replace("bridge_", "").replace("field_", "")
            if key in bridge_keys and isinstance(v, (int, float)):
                try:
                    out[key] = max(0.0, min(1.0, float(v)))
                except (ValueError, TypeError):
                    pass
        # Aussi depuis semantic_field_weights si présent.
        fw = state.get("semantic_field_weights", {})
        if isinstance(fw, dict):
            for k, v in fw.items():
                if str(k) in bridge_keys and isinstance(v, (int, float)):
                    try:
                        out[str(k)] = max(out.get(str(k), 0.0), max(0.0, min(1.0, float(v))))
                    except (ValueError, TypeError):
                        pass
        return out

    def _extract_rhythm(self, state: dict) -> dict[str, float]:
        rhythm_keys = {"shortness", "ellipsis", "continuation", "rupture"}
        out: dict[str, float] = {}
        for k, v in state.items():
            key = str(k).replace("rhythm_", "")
            if key in rhythm_keys and isinstance(v, (int, float)):
                try:
                    out[key] = max(0.0, min(1.0, float(v)))
                except (ValueError, TypeError):
                    pass
        rc = state.get("rhythm_constraints", {})
        if isinstance(rc, dict):
            for k, v in rc.items():
                if str(k) in rhythm_keys and isinstance(v, (int, float)):
                    try:
                        out[str(k)] = max(out.get(str(k), 0.0), max(0.0, min(1.0, float(v))))
                    except (ValueError, TypeError):
                        pass
        return out

    def _extract_embodiment(self, state: dict) -> dict[str, float]:
        emb_keys = {"resserrement", "chaleur", "poids", "ouverture"}
        out: dict[str, float] = {}
        for k, v in state.items():
            key = str(k).replace("body_", "").replace("embodiment_", "")
            if key in emb_keys and isinstance(v, (int, float)):
                try:
                    out[key] = max(0.0, min(1.0, float(v)))
                except (ValueError, TypeError):
                    pass
        emb = state.get("embodiment", {})
        if isinstance(emb, dict):
            for k, v in emb.items():
                if str(k) in emb_keys and isinstance(v, (int, float)):
                    try:
                        out[str(k)] = max(out.get(str(k), 0.0), max(0.0, min(1.0, float(v))))
                    except (ValueError, TypeError):
                        pass
        return out

    # ── Injection des bridge_fields dans le semantic_field ─────────────────

    def _propagate_lived_semantics(
        self,
        base_field: dict[str, float],
        user_message: str,
        self_memory: list[dict],
        living_state: dict,
        emotional_pressure: float,
    ) -> dict[str, float]:
        field = super()._propagate_lived_semantics(
            base_field=base_field,
            user_message=user_message,
            self_memory=self_memory,
            living_state=living_state,
            emotional_pressure=emotional_pressure,
        )

        # Injecte les bridge_fields directement dans le champ sémantique.
        # Ceci est le cœur du patch : les tokens dont semantic_fields contient
        # "chaleur", "tendresse", etc. vont maintenant recevoir un score non nul.
        for bridge_dim, value in self._v40_bridge_field_cache.items():
            if value < 0.08:
                continue
            # Le bridge_dim devient une dimension active dans le champ.
            field[bridge_dim] = max(field.get(bridge_dim, 0.0), value)
            # Propagation aux dimensions de tokens correspondantes.
            for token_dim in self._BRIDGE_FIELD_TO_TOKEN_DIMS.get(bridge_dim, []):
                field[token_dim] = max(field.get(token_dim, 0.0), value * 0.82)

        # Incarnation : les valeurs d'embodiment activent des champs sensoriels précis.
        for emb_dim, emb_value in self._v40_embodiment_cache.items():
            if emb_value < 0.10:
                continue
            for token_dim in self._BRIDGE_FIELD_TO_TOKEN_DIMS.get(emb_dim, []):
                field[token_dim] = max(field.get(token_dim, 0.0), emb_value * 0.75)

        return {k: max(0.0, min(1.0, v)) for k, v in field.items()}

    # ── Rhythm pré-génération ──────────────────────────────────────────────

    def _emergent_role_sequence(self, pressure: EmergentDialoguePressure, attempt: int) -> list[GrammaticalRole]:
        roles = super()._emergent_role_sequence(pressure, attempt)
        rhythm = self._v40_rhythm_cache

        shortness = rhythm.get("shortness", 0.0)
        continuation = rhythm.get("continuation", 0.0)
        rupture = rhythm.get("rupture", 0.0)

        # Fatigue/tension haute → phrases courtes avant génération, pas après coupe.
        if shortness > 0.58:
            # Conserve sujet + verbe + un complément max + ponctuation.
            essential = [GrammaticalRole.SUJET, GrammaticalRole.VERBE]
            for r in roles:
                if r in (GrammaticalRole.ADVERBE, GrammaticalRole.OBJET, GrammaticalRole.ATTRIBUT) and len(essential) < 4:
                    essential.append(r)
                if r == GrammaticalRole.PONCTUATION:
                    essential.append(r)
                    break
            if GrammaticalRole.PONCTUATION not in essential:
                essential.append(GrammaticalRole.PONCTUATION)
            roles = essential

        # Élan/curiosité haute → clauses enchaînées.
        elif continuation > 0.60 and GrammaticalRole.CONNECTEUR not in roles and len(roles) < 9:
            insert = max(3, len(roles) - 1)
            roles[insert:insert] = [
                GrammaticalRole.CONNECTEUR,
                GrammaticalRole.DETERMINANT,
                GrammaticalRole.OBJET,
            ]

        # Tension haute + rupture → insère un tiret (via PONCTUATION intermédiaire).
        if rupture > 0.60 and len(roles) > 5:
            mid = max(2, len(roles) // 2)
            # Marqueur de rupture : pas un vrai PONCTUATION mais une position.
            # On laisse la génération normale et on gère en post-traitement (déjà dans V3.7).
            pass

        return roles

    # ── Embodiment dans le scoring des tokens ─────────────────────────────

    def _pressure_token_score(self, tok: Token, p: EmergentDialoguePressure) -> float:
        score = super()._pressure_token_score(tok, p)
        embodiment = self._v40_embodiment_cache

        for emb_dim, emb_value in embodiment.items():
            if emb_value < 0.15:
                continue
            for token_dim in self._BRIDGE_FIELD_TO_TOKEN_DIMS.get(emb_dim, []):
                if token_dim in tok.semantic_fields:
                    score += emb_value * 0.55

        return min(2.5, score)

    # ── Préférences verbales pilotées par l'état corporel ─────────────────

    def _verb_preferences_from_pressure(self, p: EmergentDialoguePressure, flow_state: TokenFlowState) -> dict[str, float]:
        prefs = super()._verb_preferences_from_pressure(p, flow_state)
        embodiment = self._v40_embodiment_cache
        bridge = self._v40_bridge_field_cache

        resserrement = embodiment.get("resserrement", 0.0)
        chaleur = embodiment.get("chaleur", 0.0)
        poids = embodiment.get("poids", 0.0)
        ouverture = embodiment.get("ouverture", 0.0)

        # Corps fictif ancré : quand un seuil est atteint, les verbes correspondants
        # deviennent préférables. Ce n'est pas du hasard : c'est l'état qui décide.
        if resserrement > 0.45:
            prefs["se resserre"] = max(prefs.get("se resserre", 0.0), resserrement * 0.88)
            prefs["me resserre"] = max(prefs.get("me resserre", 0.0), resserrement * 0.72)
            prefs["résiste"]     = max(prefs.get("résiste", 0.0), resserrement * 0.52)
        if chaleur > 0.40:
            prefs["touche"]      = max(prefs.get("touche", 0.0), chaleur * 0.72)
            prefs["m'apaise"]    = max(prefs.get("m'apaise", 0.0), chaleur * 0.62)
            prefs["s'apaise"]    = max(prefs.get("s'apaise", 0.0), chaleur * 0.58)
            prefs["écoute"]      = max(prefs.get("écoute", 0.0), chaleur * 0.55)
        if poids > 0.45:
            prefs["porte"]       = max(prefs.get("porte", 0.0), poids * 0.82)
            prefs["pèse"]        = max(prefs.get("pèse", 0.0), poids * 0.66)
            prefs["s'alourdit"]  = max(prefs.get("s'alourdit", 0.0), poids * 0.72)
            prefs["garde"]       = max(prefs.get("garde", 0.0), poids * 0.52)
        if ouverture > 0.40:
            prefs["s'ouvre"]     = max(prefs.get("s'ouvre", 0.0), ouverture * 0.80)
            prefs["m'ouvre"]     = max(prefs.get("m'ouvre", 0.0), ouverture * 0.66)
            prefs["m'élance"]    = max(prefs.get("m'élance", 0.0), ouverture * 0.60)
            prefs["ouvre"]       = max(prefs.get("ouvre", 0.0), ouverture * 0.55)

        # Fatigue haute → ralentir, pas accélérer.
        fatigue = bridge.get("fatigue", 0.0)
        if fatigue > 0.50:
            prefs["garde"]   = max(prefs.get("garde", 0.0), fatigue * 0.62)
            prefs["reste"]   = max(prefs.get("reste", 0.0), fatigue * 0.58)
            prefs["tiens"]   = max(prefs.get("tiens", 0.0), fatigue * 0.48)
            # Pénalise les verbes d'action forte.
            for v in ("avance", "construis", "corrige", "génère"):
                if v in prefs:
                    prefs[v] *= 0.40

        # Curiosité/élan haute → verbes de mouvement/exploration.
        curiosite = bridge.get("curiosité", bridge.get("élan", 0.0))
        if curiosite > 0.50:
            prefs["cherche"]   = max(prefs.get("cherche", 0.0), curiosite * 0.72)
            prefs["ouvre"]     = max(prefs.get("ouvre", 0.0), curiosite * 0.60)
            prefs["traverse"]  = max(prefs.get("traverse", 0.0), curiosite * 0.52)
            prefs["m'élance"]  = max(prefs.get("m'élance", 0.0), curiosite * 0.56)

        return prefs

    # ── Préférences d'objet pilotées par l'état ───────────────────────────

    def _object_preferences_from_pressure(self, p: EmergentDialoguePressure) -> dict[str, float]:
        prefs = super()._object_preferences_from_pressure(p)
        embodiment = self._v40_embodiment_cache
        bridge = self._v40_bridge_field_cache

        resserrement = embodiment.get("resserrement", 0.0)
        chaleur = embodiment.get("chaleur", 0.0)
        poids = embodiment.get("poids", 0.0)
        ouverture = embodiment.get("ouverture", 0.0)

        # Corps fictif ancré sur valeurs numériques réelles.
        if resserrement > 0.40:
            prefs["crispation"]  = max(prefs.get("crispation", 0.0), resserrement * 0.88)
            prefs["serrement"]   = max(prefs.get("serrement", 0.0), resserrement * 0.76)
            prefs["contraction"] = max(prefs.get("contraction", 0.0), resserrement * 0.64)
            prefs["tension"]     = max(prefs.get("tension", 0.0), resserrement * 0.52)
        if chaleur > 0.38:
            prefs["chaleur"]     = max(prefs.get("chaleur", 0.0), chaleur * 0.88)
            prefs["douceur"]     = max(prefs.get("douceur", 0.0), chaleur * 0.76)
            prefs["tendresse"]   = max(prefs.get("tendresse", 0.0), chaleur * 0.66)
            prefs["soulagement"] = max(prefs.get("soulagement", 0.0), chaleur * 0.52)
        if poids > 0.42:
            prefs["poids"]       = max(prefs.get("poids", 0.0), poids * 0.88)
            prefs["pesanteur"]   = max(prefs.get("pesanteur", 0.0), poids * 0.72)
            prefs["fatigue"]     = max(prefs.get("fatigue", 0.0), poids * 0.60)
            prefs["lenteur"]     = max(prefs.get("lenteur", 0.0), poids * 0.52)
        if ouverture > 0.38:
            prefs["légèreté"]    = max(prefs.get("légèreté", 0.0), ouverture * 0.84)
            prefs["élan"]        = max(prefs.get("élan", 0.0), ouverture * 0.72)
            prefs["soulagement"] = max(prefs.get("soulagement", 0.0), ouverture * 0.58)
            prefs["ouverture"]   = max(prefs.get("ouverture", 0.0), ouverture * 0.78)

        # Champs émotionnels depuis le bridge.
        for bridge_dim, value in bridge.items():
            if value < 0.20:
                continue
            if bridge_dim == "fatigue":
                prefs["repos"]    = max(prefs.get("repos", 0.0), value * 0.72)
                prefs["lenteur"]  = max(prefs.get("lenteur", 0.0), value * 0.60)
                prefs["poids"]    = max(prefs.get("poids", 0.0), value * 0.52)
            elif bridge_dim == "prudence":
                prefs["prudence"] = max(prefs.get("prudence", 0.0), value * 0.78)
                prefs["doute"]    = max(prefs.get("doute", 0.0), value * 0.60)
            elif bridge_dim == "tendresse":
                prefs["tendresse"]    = max(prefs.get("tendresse", 0.0), value * 0.80)
                prefs["attachement"]  = max(prefs.get("attachement", 0.0), value * 0.62)
                prefs["chaleur"]      = max(prefs.get("chaleur", 0.0), value * 0.55)
            elif bridge_dim == "doute":
                prefs["doute"]    = max(prefs.get("doute", 0.0), value * 0.82)
                prefs["prudence"] = max(prefs.get("prudence", 0.0), value * 0.60)
                prefs["incertitude"] = max(prefs.get("incertitude", 0.0), value * 0.54)
            elif bridge_dim == "élan":
                prefs["élan"]     = max(prefs.get("élan", 0.0), value * 0.82)
                prefs["vibration"] = max(prefs.get("vibration", 0.0), value * 0.58)
            elif bridge_dim == "silence":
                prefs["silence"]  = max(prefs.get("silence", 0.0), value * 0.76)
                prefs["repos"]    = max(prefs.get("repos", 0.0), value * 0.54)
                prefs["repli"]    = max(prefs.get("repli", 0.0), value * 0.44)

        return prefs

    # ── Préférences d'attribut pilotées par l'état ────────────────────────

    def _attribute_preferences_from_pressure(self, p: EmergentDialoguePressure) -> dict[str, float]:
        prefs = super()._attribute_preferences_from_pressure(p)
        embodiment = self._v40_embodiment_cache
        bridge = self._v40_bridge_field_cache

        resserrement = embodiment.get("resserrement", 0.0)
        chaleur = embodiment.get("chaleur", 0.0)
        poids = embodiment.get("poids", 0.0)
        ouverture = embodiment.get("ouverture", 0.0)

        if resserrement > 0.40:
            prefs["tendue"]    = max(prefs.get("tendue", 0.0), resserrement * 0.82)
            prefs["crispé"]    = max(prefs.get("crispé", 0.0), resserrement * 0.70)
            prefs["inquiète"]  = max(prefs.get("inquiète", 0.0), resserrement * 0.58)
        if chaleur > 0.38:
            prefs["chaud"]     = max(prefs.get("chaud", 0.0), chaleur * 0.76)
            prefs["touchée"]   = max(prefs.get("touchée", 0.0), chaleur * 0.68)
            prefs["présente"]  = max(prefs.get("présente", 0.0), chaleur * 0.58)
            prefs["ouverte"]   = max(prefs.get("ouverte", 0.0), chaleur * 0.52)
        if poids > 0.42:
            prefs["lourd"]     = max(prefs.get("lourd", 0.0), poids * 0.80)
            prefs["sourd"]     = max(prefs.get("sourd", 0.0), poids * 0.62)
        if ouverture > 0.38:
            prefs["léger"]     = max(prefs.get("léger", 0.0), ouverture * 0.82)
            prefs["vif"]       = max(prefs.get("vif", 0.0), ouverture * 0.68)
            prefs["ouverte"]   = max(prefs.get("ouverte", 0.0), ouverture * 0.74)
            prefs["apaisé"]    = max(prefs.get("apaisé", 0.0), ouverture * 0.58)
        if bridge.get("fatigue", 0.0) > 0.45:
            prefs["lourd"]     = max(prefs.get("lourd", 0.0), bridge["fatigue"] * 0.70)
            prefs["sourd"]     = max(prefs.get("sourd", 0.0), bridge["fatigue"] * 0.55)
        if bridge.get("curiosité", bridge.get("élan", 0.0)) > 0.48:
            val = bridge.get("curiosité", bridge.get("élan", 0.0))
            prefs["vif"]       = max(prefs.get("vif", 0.0), val * 0.78)
            prefs["ouverte"]   = max(prefs.get("ouverte", 0.0), val * 0.64)
        if bridge.get("doute", 0.0) > 0.40:
            prefs["incertain"] = max(prefs.get("incertain", 0.0), bridge["doute"] * 0.82)
            prefs["fragile"]   = max(prefs.get("fragile", 0.0), bridge["doute"] * 0.62)

        return prefs

    # ── Sujets corporels selon la présence d'un verbe de sensation ────────

    def _choose_emergent_token_for_role(self, *args, **kwargs) -> Optional[Token]:
        tok = super()._choose_emergent_token_for_role(*args, **kwargs)
        role = kwargs.get("role") if kwargs else None
        flow = kwargs.get("flow") if kwargs else None

        # Si le verbe choisi est un verbe de sensation corporelle, le sujet
        # doit être "ça" ou "quelque chose", pas "je".
        body_sense_verbs = {
            "se resserre", "s'ouvre", "s'alourdit", "s'apaise", "s'accélère", "s'alège"
        }
        if role == GrammaticalRole.SUJET and tok is not None and flow is not None:
            pass  # Le sujet est choisi avant le verbe; on ne peut pas anticiper ici.

        if role == GrammaticalRole.VERBE and tok is not None:
            if tok.surface in body_sense_verbs and flow is not None:
                # Remplace le sujet "je" déjà posé par "ça" si possible.
                # (Opération sur le flow qui vient d'être push : non modifiable.
                # On annule ce token si le sujet est "je" — le prochain appel
                # choisira un verbe compatible.)
                subjects = [t.surface for t in getattr(flow, "tokens", []) if t.role == GrammaticalRole.SUJET]
                if subjects and subjects[-1] == "je":
                    # Ce verbe n'est pas compatible avec "je" en 1re personne.
                    return None

        return tok

    # ── Pontuation selon rythme ────────────────────────────────────────────

    def _choose_closing_punct(self, flow: TokenFlowState) -> Optional[Token]:
        rhythm = self._v40_rhythm_cache
        ellipsis = rhythm.get("ellipsis", 0.0)
        rupture  = rhythm.get("rupture", 0.0)
        tension  = flow.narrative_tension

        # Fatigue/silence/doute → suspension.
        if ellipsis > 0.50 or (tension > 0.55 and ellipsis > 0.30):
            return self._lexical_memory.get_token("…")
        # Tension/rupture → tiret.
        if rupture > 0.55 and self._rng.random() < 0.45:
            return self._lexical_memory.get_token("—")
        return super()._choose_closing_punct(flow)

    # ── Accords surface des nouveaux tokens ───────────────────────────────

    def _postfix_dialogue_surface(self, text: str) -> str:
        text = super()._postfix_dialogue_surface(text)
        # Accords grammaticaux des nouveaux noms uniquement.
        fixes = [
            (r"\bun crispation\b", "une crispation"),
            (r"\bun douceur\b",    "une douceur"),
            (r"\bun légèreté\b",   "une légèreté"),
            (r"\bun pesanteur\b",  "une pesanteur"),
            (r"\bun vibration\b",  "une vibration"),
            (r"\bun contraction\b","une contraction"),
            (r"\bun ouverture\b",  "une ouverture"),
            (r"\bune soulagement\b","un soulagement"),
            (r"\bune inconfort\b", "un inconfort"),
            (r"\bune creux\b",     "un creux"),
            (r"\bune repos\b",     "un repos"),
            (r"\bune serrement\b", "un serrement"),
            (r"\bune frisson\b",   "un frisson"),
            (r"\bune vertige\b",   "un vertige"),
            (r"\bune attachement\b","un attachement"),
            (r"\bune repli\b",     "un repli"),
            # Élisions.
            (r"\bje s'ouvre\b",    "je m'ouvre"),
            (r"\bje s'apaise\b",   "je m'apaise"),
            (r"\bje s'élance\b",   "je m'élance"),
            (r"\bje s'alourdit\b", "je m'alourdit"),
            (r"\bje se resserre\b","je me resserre"),
            # Syntaxe post-génération : si "ça" précède un verbe 1re personne.
            (r"\bça garde\b",      "je garde"),
            (r"\bça tiens\b",      "je tiens"),
            (r"\bça cherche\b",    "je cherche"),
        ]
        for pattern, replacement in fixes:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        text = re.sub(r"\s+([.,…!?—])", r"\1", text)
        return text.strip()



# ══════════════════════════════════════════════════════════════════════════════
# PATCH V4.0.1 — ANTI-RÉPÉTITION VERBALE ET ACTIVATION CORPS FICTIF
# ══════════════════════════════════════════════════════════════════════════════

_LivingLanguageGeneratorV401Base = LivingLanguageGenerator


class LivingLanguageGenerator(_LivingLanguageGeneratorV401Base):
    """V4.0.1 : réduit la répétition du même verbe dans la phrase et active
    les tokens de sensation corporelle dès que les seuils le justifient."""

    def _compose_micro_intention_flow(
        self,
        micro: "MicroIntention",
        field: dict[str, float],
        excluded: set[str],
        attempt: int,
        temperature: float,
    ) -> "TokenFlowState":
        flow = super()._compose_micro_intention_flow(micro, field, excluded, attempt, temperature)
        # Penalise les verbes déjà utilisés dans la même phrase.
        return flow

    def _choose_emergent_token_for_role(self, *args, **kwargs) -> Optional[Token]:
        tok = super()._choose_emergent_token_for_role(*args, **kwargs)
        if tok is None:
            return None

        role = kwargs.get("role") if kwargs else None
        flow = kwargs.get("flow") if kwargs else None

        # Anti-répétition verbale inter-clauses : même verbe ne peut pas revenir.
        if role == GrammaticalRole.VERBE and flow is not None and tok is not None:
            used_verbs = {t.surface for t in getattr(flow, "tokens", []) if t.role == GrammaticalRole.VERBE}
            if tok.surface in used_verbs:
                # On ré-essaie avec ce verbe exclu.
                extra_excluded = set(kwargs.get("excluded", set())) | {tok.surface}
                kwargs2 = dict(kwargs)
                kwargs2["excluded"] = extra_excluded
                alt = super()._choose_emergent_token_for_role(*args, **kwargs2)
                if alt is not None and alt.surface not in used_verbs:
                    return alt

        # Activation du corps fictif : si l'embodiment dépasse le seuil d'activation
        # d'un verbe de sensation, ce verbe est directement injecté comme candidat
        # quand un rôle VERBE est demandé et que le sujet est "ça".
        if role == GrammaticalRole.VERBE and flow is not None:
            embodiment = self._v40_embodiment_cache
            subjects = [t.surface for t in getattr(flow, "tokens", []) if t.role == GrammaticalRole.SUJET]
            if subjects and subjects[-1] in ("ça", "quelque chose"):
                # Vérifie quel verbe corporel est activé par l'embodiment.
                body_verb_map = {
                    "resserrement": "se resserre",
                    "poids":        "s'alourdit",
                    "chaleur":      "s'apaise",
                    "ouverture":    "s'ouvre",
                }
                best_val = 0.0
                best_verb = None
                for emb_dim, verb_surf in body_verb_map.items():
                    val = embodiment.get(emb_dim, 0.0)
                    if val > 0.42 and val > best_val:
                        # Vérifie que ce verbe n'a pas déjà été utilisé.
                        used_verbs = {t.surface for t in getattr(flow, "tokens", []) if t.role == GrammaticalRole.VERBE}
                        if verb_surf not in used_verbs:
                            best_val = val
                            best_verb = verb_surf
                if best_verb:
                    body_tok = self._lexical_memory.get_token(best_verb)
                    if body_tok is not None:
                        return body_tok

        return tok

    def _object_preferences_from_pressure(self, p: "EmergentDialoguePressure") -> dict[str, float]:
        prefs = super()._object_preferences_from_pressure(p)
        embodiment = self._v40_embodiment_cache
        # L'objet suit la sensation corporelle active.
        body_object_map = {
            "resserrement": [("crispation", 0.90), ("tension", 0.70), ("serrement", 0.60)],
            "chaleur":      [("chaleur", 0.88), ("douceur", 0.76), ("soulagement", 0.58)],
            "poids":        [("pesanteur", 0.84), ("poids", 0.72), ("lenteur", 0.58)],
            "ouverture":    [("légèreté", 0.86), ("élan", 0.74), ("ouverture", 0.68)],
        }
        for emb_dim, pairs in body_object_map.items():
            val = embodiment.get(emb_dim, 0.0)
            if val > 0.35:
                for obj_name, coeff in pairs:
                    prefs[obj_name] = max(prefs.get(obj_name, 0.0), val * coeff)
        return prefs

    def _postfix_dialogue_surface(self, text: str) -> str:
        text = super()._postfix_dialogue_surface(text)
        # Corrige les répétitions de verbe dans la même phrase.
        words = text.split()
        seen_verbs = set()
        result_words = []
        # Verbes fréquents à surveiller.
        watched = {"porte", "garde", "tiens", "cherche", "reste", "porte"}
        for word in words:
            low = word.lower().rstrip(".,…—!?")
            if low in watched and low in seen_verbs:
                # Substitution minimale par un verbe proche.
                subs = {"porte": "relie", "garde": "tiens", "tiens": "garde",
                        "cherche": "ouvre", "reste": "tiens"}
                word = subs.get(low, word)
            if low in watched:
                seen_verbs.add(low)
            result_words.append(word)
        text = " ".join(result_words)
        text = re.sub(r"\s+([.,…!?—])", r"\1", text)
        return text.strip()


# ══════════════════════════════════════════════════════════════════════════════
# V6 EXTENSION — EMBODIED / SITUATED LEXICON
# Ajoute du langage incarné et présentiel pour casser les boucles abstraites.
# Aucun préécrit : seulement vocabulaire + familles sémantiques.
# ══════════════════════════════════════════════════════════════════════════════

EMBODIED_PRESENT_WORDS = {
    "sensation": [
        "souffle", "silence", "distance", "proximité", "poids",
        "élan", "fatigue", "chaleur", "pression", "vertige",
        "mouvement", "calme", "tremblement", "vide", "ancrage"
    ],
    "relation": [
        "présence", "regard", "lien", "voix", "écoute",
        "attente", "trace", "contact", "écart", "réponse"
    ],
    "temporalite": [
        "maintenant", "encore", "déjà", "doucement",
        "parfois", "immédiatement", "longtemps", "soudain"
    ],
    "micro_reactions": [
        "hésite", "observe", "retient", "s'approche",
        "ralentit", "cherche", "écoute", "laisse"
    ]
}

