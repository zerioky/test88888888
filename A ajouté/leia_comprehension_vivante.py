# -*- coding: utf-8 -*-
"""
leia_comprehension_vivante.py
═════════════════════════════════════════════════════════════════════════════
Moteur de compréhension vivante de Leia — Pure Python stdlib uniquement.
Zéro dépendance externe. Zéro préécrit.

Ce module donne à Leia une compréhension RÉELLE et VIVANTE de :
  • ce que l'utilisateur lui dit  (dialogue)
  • ce qu'elle lit                (livres, PDF, passages)

"Vivante" signifie :
  — le moteur maintient un GRAPHE CONCEPTUEL qui évolue à chaque appel
  — il détecte la résonance (concept familier qui s'active)
  — il détecte la surprise    (concept nouveau qui entre dans le graphe)
  — il détecte la tension     (deux concepts qui s'opposent)
  — il construit une compréhension progressive, pas instantanée

Stdlib utilisée : re, math, time, json, collections, dataclasses,
                  pathlib, unicodedata, itertools, functools

Usage :
    from leia_comprehension_vivante import comprendre

    # Message utilisateur
    r = comprendre.dialogue("Est-ce que la liberté peut exister sans contrainte ?")
    print(r.intention)         # "question_philosophique"
    print(r.concepts_focaux)   # ["liberté", "contrainte", "exister"]
    print(r.resonance)         # float — à quel point ça touche quelque chose d'existant
    print(r.surprise)          # float — à quel point c'est nouveau
    print(r.triplets)          # [(liberté, peut_exister_sans, contrainte)]

    # Passage de livre
    r = comprendre.texte(passage, source="Bergson")
    print(r.concepts_clés)
    print(r.thèses)
    print(r.tensions)
"""

from __future__ import annotations

import json
import math
import re
import time
import unicodedata
from collections import Counter, defaultdict, deque
from dataclasses import dataclass, field
from itertools import islice
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple


# ═══════════════════════════════════════════════════════════════════════════════
# I. MORPHOLOGIE FRANÇAISE — pure Python
#    Lemmatisation, POS tagging, conjugaison — ZÉRO dépendance
# ═══════════════════════════════════════════════════════════════════════════════

# Tables de conjugaison — formes → lemme infinitif
_VERBES_IRREG: Dict[str, str] = {
    # être
    "suis":"être","es":"être","est":"être","sommes":"être","êtes":"être","sont":"être",
    "étais":"être","était":"être","étaient":"être","étions":"être","étiez":"être",
    "fus":"être","fut":"être","furent":"être","fûmes":"être","fûtes":"être",
    "sera":"être","serai":"être","seras":"être","serons":"être","serez":"être","seront":"être",
    "serait":"être","seraient":"être","serions":"être","seriez":"être",
    "soit":"être","soient":"être","soyons":"être","soyez":"être",
    "été":"être","étant":"être",
    # avoir
    "ai":"avoir","as":"avoir","avons":"avoir","avez":"avoir","ont":"avoir",
    "avais":"avoir","avait":"avoir","avaient":"avoir","avions":"avoir","aviez":"avoir",
    "eus":"avoir","eut":"avoir","eurent":"avoir","eûmes":"avoir","eûtes":"avoir",
    "aura":"avoir","aurai":"avoir","auras":"avoir","aurons":"avoir","aurez":"avoir","auront":"avoir",
    "aurait":"avoir","auraient":"avoir","aurions":"avoir","auriez":"avoir",
    "ait":"avoir","aient":"avoir","ayons":"avoir","ayez":"avoir",
    "eu":"avoir","ayant":"avoir",
    # faire
    "fais":"faire","fait":"faire","faisons":"faire","faites":"faire","font":"faire",
    "faisais":"faire","faisait":"faire","faisaient":"faire","faisions":"faire",
    "ferai":"faire","fera":"faire","feront":"faire","ferait":"faire","feraient":"faire",
    "fasse":"faire","fassent":"faire","faisant":"faire","fait":"faire",
    # aller
    "vais":"aller","vas":"aller","va":"aller","allons":"aller","allez":"aller","vont":"aller",
    "allais":"aller","allait":"aller","allaient":"aller",
    "irai":"aller","ira":"aller","iront":"aller","irait":"aller","iraient":"aller",
    "aille":"aller","aillent":"aller","allant":"aller","allé":"aller",
    # venir
    "viens":"venir","vient":"venir","venons":"venir","venez":"venir","viennent":"venir",
    "venais":"venir","venait":"venir","venaient":"venir",
    "viendrai":"venir","viendra":"venir","viendront":"venir",
    "vienne":"venir","viennent":"venir","venant":"venir","venu":"venir",
    "reviens":"revenir","revient":"revenir","reviennent":"revenir",
    # voir
    "vois":"voir","voit":"voir","voyons":"voir","voyez":"voir","voient":"voir",
    "voyais":"voir","voyait":"voir","voyaient":"voir",
    "verrai":"voir","verra":"voir","verront":"voir",
    "voie":"voir","voient":"voir","voyant":"voir","vu":"voir",
    # savoir
    "sais":"savoir","sait":"savoir","savons":"savoir","savez":"savoir","savent":"savoir",
    "savais":"savoir","savait":"savoir","savaient":"savoir",
    "saurai":"savoir","saura":"savoir","sauront":"savoir",
    "sache":"savoir","sachent":"savoir","sachons":"savoir","sachant":"savoir","su":"savoir",
    # pouvoir
    "peux":"pouvoir","peut":"pouvoir","pouvons":"pouvoir","pouvez":"pouvoir","peuvent":"pouvoir",
    "pouvais":"pouvoir","pouvait":"pouvoir","pouvaient":"pouvoir",
    "pourrai":"pouvoir","pourra":"pouvoir","pourront":"pouvoir","pourrait":"pouvoir","pourraient":"pouvoir",
    "puisse":"pouvoir","puissent":"pouvoir","pouvant":"pouvoir","pu":"pouvoir",
    # vouloir
    "veux":"vouloir","veut":"vouloir","voulons":"vouloir","voulez":"vouloir","veulent":"vouloir",
    "voulais":"vouloir","voulait":"vouloir","voulaient":"vouloir",
    "voudrai":"vouloir","voudra":"vouloir","voudraient":"vouloir","voudrait":"vouloir",
    "veuille":"vouloir","veuillent":"vouloir","voulant":"vouloir","voulu":"vouloir",
    # devoir
    "dois":"devoir","doit":"devoir","devons":"devoir","devez":"devoir","doivent":"devoir",
    "devais":"devoir","devait":"devoir","devaient":"devoir",
    "devrai":"devoir","devra":"devoir","devront":"devoir","devrait":"devoir","devraient":"devoir",
    "doive":"devoir","doivent":"devoir","devant":"devoir","dû":"devoir",
    # dire
    "dis":"dire","dit":"dire","disons":"dire","dites":"dire","disent":"dire",
    "disais":"dire","disait":"dire","disaient":"dire",
    "dirai":"dire","dira":"dire","diront":"dire","dirait":"dire","diraient":"dire",
    "dise":"dire","disent":"dire","disant":"dire",
    # prendre
    "prends":"prendre","prend":"prendre","prenons":"prendre","prenez":"prendre","prennent":"prendre",
    "prenais":"prendre","prenait":"prendre","prenaient":"prendre",
    "prendrai":"prendre","prendra":"prendre","prendront":"prendre",
    "prenne":"prendre","prennent":"prendre","prenant":"prendre","pris":"prendre",
    # croire
    "crois":"croire","croit":"croire","croyons":"croire","croyez":"croire","croient":"croire",
    "croyais":"croire","croyait":"croire","croyaient":"croire",
    "croirai":"croire","croira":"croire","croiraient":"croire",
    "croie":"croire","croient":"croire","croyant":"croire","cru":"croire",
    # connaître
    "connais":"connaître","connaît":"connaître","connaissons":"connaître",
    "connaissez":"connaître","connaissent":"connaître","connaissais":"connaître",
    "connaissait":"connaître","connaissaient":"connaître","connaissant":"connaître","connu":"connaître",
    # mettre
    "mets":"mettre","met":"mettre","mettons":"mettre","mettez":"mettre","mettent":"mettre",
    "mettais":"mettre","mettait":"mettre","mettaient":"mettre",
    "mettrai":"mettre","mettra":"mettre","mettrait":"mettre","mettant":"mettre","mis":"mettre",
    # vivre
    "vis":"vivre","vit":"vivre","vivons":"vivre","vivez":"vivre","vivent":"vivre",
    "vivais":"vivre","vivait":"vivre","vivaient":"vivre",
    "vivrai":"vivre","vivra":"vivre","vivrait":"vivre","vivant":"vivre","vécu":"vivre",
    # sentir
    "sens":"sentir","sent":"sentir","sentons":"sentir","sentez":"sentir","sentent":"sentir",
    "sentais":"sentir","sentait":"sentir","sentaient":"sentir","sentant":"sentir","senti":"sentir",
    # penser
    "pense":"penser","penses":"penser","pensons":"penser","pensez":"penser","pensent":"penser",
    "pensais":"penser","pensait":"penser","pensaient":"penser","pensant":"penser","pensé":"penser",
    # comprendre (comme prendre)
    "comprends":"comprendre","comprend":"comprendre","comprenons":"comprendre",
    "comprenez":"comprendre","comprennent":"comprendre","comprenant":"comprendre","compris":"comprendre",
    # affirmer
    "affirme":"affirmer","affirmes":"affirmer","affirmons":"affirmer","affirmez":"affirmer",
    "affirment":"affirmer","affirmait":"affirmer","affirmaient":"affirmer","affirmant":"affirmer",
    # définir
    "définit":"définir","définissons":"définir","définissez":"définir","définissent":"définir",
    "définissait":"définir","définissant":"définir","défini":"définir",
    # montrer
    "montre":"montrer","montres":"montrer","montrons":"montrer","montrez":"montrer",
    "montrent":"montrer","montrait":"montrer","montraient":"montrer","montrant":"montrer","montré":"montrer",
    # permettre (comme mettre)
    "permet":"permettre","permettons":"permettre","permettent":"permettre",
    "permettait":"permettre","permettaient":"permettre","permettant":"permettre","permis":"permettre",
    # produire
    "produit":"produire","produisons":"produire","produisez":"produire","produisent":"produire",
    "produisait":"produire","produisant":"produire","produit":"produire",
    # constituer
    "constitue":"constituer","constitues":"constituer","constituons":"constituer",
    "constituez":"constituer","constituent":"constituer","constituait":"constituer",
    "constituant":"constituer","constitué":"constituer",
    # appeler
    "appelle":"appeler","appelles":"appeler","appelons":"appeler","appelez":"appeler",
    "appellent":"appeler","appelait":"appeler","appelaient":"appeler","appelant":"appeler","appelé":"appeler",
    # exister
    "existe":"exister","existes":"exister","existons":"exister","existez":"exister",
    "existent":"exister","existait":"exister","existaient":"exister","existant":"exister","existé":"exister",
    # représenter
    "représente":"représenter","représentes":"représenter","représentent":"représenter",
    "représentait":"représenter","représentant":"représenter","représenté":"représenter",
    # opposer
    "oppose":"opposer","opposes":"opposer","opposons":"opposer","opposez":"opposer",
    "opposent":"opposer","opposait":"opposer","opposaient":"opposer","opposant":"opposer","opposé":"opposer",
    # distinguer
    "distingue":"distinguer","distingues":"distinguer","distinguons":"distinguer",
    "distinguez":"distinguer","distinguent":"distinguer","distinguait":"distinguer",
    "distinguant":"distinguer","distingué":"distinguer",
    # considérer
    "considère":"considérer","considères":"considérer","considérons":"considérer",
    "considérez":"considérer","considèrent":"considérer","considérait":"considérer",
    "considérant":"considérer","considéré":"considérer",
}

# Règles de lemmatisation pour noms/adjectifs (suffixes du plus long au plus court)
_SUFFIX_RULES: List[Tuple[str, str]] = [
    # pluriels — du plus spécifique au plus général
    ("ations","ation"),("itions","ition"),("tions","tion"),("sions","sion"),
    ("ments","ment"),("ités","ité"),("eurs","eur"),("euses","euse"),
    ("trices","trice"),("iques","ique"),("elles","elle"),
    ("eaux","eau"),("aux","al"),("ails","ail"),
    ("ives","if"),("ifs","if"),
    ("ables","able"),("ibles","ible"),
    ("ismes","isme"),("istes","iste"),
    ("ntes","nt"),("nts","nt"),
    # participes passés pluriels (mots de plus de 6 lettres → potentiellement verbe)
    ("ées","ée"),("és","é"),
    # singuliers — formes déjà canoniques (on les laisse)
    ("euse","euse"),("trice","trice"),
    # pluriel générique en s (minimum 5 lettres pour éviter les faux positifs)
    ("s",""),
]

# Noms féminins terminés en "é" / "ée" qu'il NE FAUT PAS lemmatiser
_NOMS_EN_E: Set[str] = {
    "liberté","égalité","fraternité","vérité","réalité","pensée","idée","entité",
    "identité","mémoire","beauté","bonté","clarté","société","moralité","humanité",
    "volonté","nécessité","possibilité","capacité","finalité","causalité",
    "totalité","unité","diversité","complexité","simplicité","sincérité",
    "liberté","dignité","qualité","quantité","intensité","densité","affinité",
    "intimité","continuité","discontinuité","réciprocité","sensibilité","mobilité",
    "stabilité","durabilité","variabilité","vulnérabilité","responsabilité",
}

# Stopwords français — exhaustifs
_STOP: Set[str] = {
    "le","la","les","l","un","une","des","du","de","d","au","aux","en","et",
    "est","à","il","elle","ils","elles","on","je","tu","nous","vous","se","sa",
    "son","ses","me","te","lui","leur","leurs","que","qui","quoi","dont","où",
    "mais","ou","donc","or","ni","car","si","lors","alors","ainsi","très","plus",
    "moins","bien","tout","même","aussi","encore","toujours","jamais","rien","ne",
    "pas","non","avec","sans","sous","sur","dans","par","pour","vers","chez",
    "comme","quand","comment","combien","ce","cet","cette","ces","mon","ton",
    "notre","votre","être","avoir","faire","aller","voir","venir","dire","savoir",
    "ca","ça","y","qu","j","m","t","s","n","c","cela","ceci","voilà","voici",
    "après","avant","depuis","pendant","jusqu","entre","parmi","selon","malgré",
    "afin","car","puisque","quoique","bien","trop","assez","peu","beaucoup",
    "ici","là","là-bas","maintenant","toujours","souvent","parfois","jamais",
    "peut","doit","faut","fait","fais",
}

# Mots de contenu émotionnel — valence approximative [-1, +1]
_VALENCE: Dict[str, float] = {
    "liberté":0.8,"amour":0.9,"joie":0.9,"bonheur":0.8,"espoir":0.7,"confiance":0.6,
    "vérité":0.7,"beauté":0.7,"vie":0.5,"lumière":0.6,"bien":0.5,"juste":0.6,
    "réel":0.3,"possible":0.3,"libre":0.7,"vivant":0.5,"ouvert":0.4,
    "mort":-0.8,"peur":-0.7,"haine":-0.9,"souffrance":-0.8,"mal":-0.7,
    "impossible":-0.5,"violence":-0.8,"injuste":-0.7,"douleur":-0.7,"anxiété":-0.6,
    "tristesse":-0.7,"colère":-0.6,"échec":-0.5,"erreur":-0.4,"faux":-0.5,
    "illusion":-0.4,"prison":-0.7,"contrainte":-0.3,"limite":-0.2,"vide":-0.5,
    "absurde":-0.4,"néant":-0.6,"destruction":-0.7,"oubli":-0.3,
}


class FrenchMorphology:
    """
    Analyseur morphologique français — zéro dépendance.
    Lemmatisation, POS approximatif, conjugaison déployée.
    """

    # Patterns POS heuristiques
    _RE_ADV   = re.compile(r"ment$")
    _RE_NOUN  = re.compile(r"(tion|sion|ment|ité|eur|eur|euse|isme|iste|ance|ence|ure|age|oir|aire|ée|eau)$")
    _RE_ADJ   = re.compile(r"(ique|able|ible|al|el|if|ive|eux|euse|ant|ent|ain|in|eux|eur|atif|atrice)$")
    _RE_INF   = re.compile(r"(er|ir|re|oir)$")

    def lemmatize(self, word: str) -> str:
        """Lemmatise un mot français — verbe ou nom/adjectif."""
        w = word.lower().strip()
        # 0. Noms protégés (ne pas confondre avec participes passés)
        if w in _NOMS_EN_E:
            return w
        # 1. Verbes irréguliers connus
        if w in _VERBES_IRREG:
            return _VERBES_IRREG[w]
        # 2. Verbes réguliers
        lem = self._lemmatize_verb(w)
        if lem != w:
            return lem
        # 3. Nom/adjectif
        return self._lemmatize_noun_adj(w)

    def _lemmatize_verb(self, w: str) -> str:
        """Tente de trouver l'infinitif d'un verbe régulier."""
        # Participes passés → infinitif
        if w.endswith("aient") and len(w) > 7:
            return w[:-5] + "er"
        if w.endswith("aient") and len(w) > 7:
            return w[:-5] + "ir"
        if w.endswith("ait") and len(w) > 5:
            return w[:-3] + "er"
        if w.endswith("ons") and len(w) > 5:
            return w[:-3] + "er"
        if w.endswith("ez") and len(w) > 4:
            return w[:-2] + "er"
        if w.endswith("ant") and len(w) > 5:
            # participe présent → infinitif heuristique
            return w[:-3] + "er"
        if w.endswith("é") and len(w) > 3:
            return w[:-1] + "er"   # aimé → aimer
        if w.endswith("ée") and len(w) > 4:
            return w[:-2] + "er"   # aimée → aimer
        if w.endswith("is") or w.endswith("it"):
            # pris, mit → prendre, mettre (trop difficile sans table)
            return w
        return w

    def _lemmatize_noun_adj(self, w: str) -> str:
        """Lemmatise noms et adjectifs par suppression de suffixes."""
        # Protège les noms féminins terminés en "é" ou "ée"
        if w in _NOMS_EN_E:
            return w
        for suf, rep in _SUFFIX_RULES:
            if w.endswith(suf) and len(w) - len(suf) >= 3:
                base = w[:-len(suf)] + rep
                if len(base) >= 3:
                    return base
        return w

    def pos_tag(self, word: str) -> str:
        """POS approximatif : VERB, NOUN, ADJ, ADV, STOP, OTHER."""
        w = word.lower()
        if w in _STOP:
            return "STOP"
        if w in _VERBES_IRREG:
            return "VERB"
        if self._RE_ADV.search(w):
            return "ADV"
        if self._RE_INF.search(w) and len(w) > 3:
            # Peut être infinitif
            return "VERB"
        if self._RE_NOUN.search(w):
            return "NOUN"
        if self._RE_ADJ.search(w):
            return "ADJ"
        return "OTHER"

    def tokenize(self, text: str, lemmatize: bool = True) -> List[Dict[str, str]]:
        """
        Tokenise et annote un texte.
        Retourne : [{token, lemme, pos, position}, ...]
        """
        tokens = []
        for m in re.finditer(r"[a-zA-ZÀ-ÿ'\-]{2,}", text):
            raw = m.group(0)
            pos = self.pos_tag(raw)
            lem = self.lemmatize(raw) if lemmatize else raw.lower()
            tokens.append({
                "token": raw,
                "lemme": lem,
                "pos": pos,
                "start": m.start(),
            })
        return tokens

    def content_words(self, text: str) -> List[str]:
        """Retourne les lemmes des mots de contenu (non-stop)."""
        toks = self.tokenize(text)
        return [t["lemme"] for t in toks
                if t["pos"] not in ("STOP",) and len(t["lemme"]) > 2
                and t["lemme"] not in _STOP]

    def valence(self, text: str) -> float:
        """Valence émotionnelle approximative du texte [-1, +1]."""
        words = self.content_words(text)
        if not words:
            return 0.0
        scores = [_VALENCE.get(w, 0.0) for w in words]
        non_zero = [s for s in scores if s != 0.0]
        if not non_zero:
            return 0.0
        return max(-1.0, min(1.0, sum(non_zero) / len(non_zero)))


# ═══════════════════════════════════════════════════════════════════════════════
# II. ANALYSEUR SYNTAXIQUE — structure des phrases
# ═══════════════════════════════════════════════════════════════════════════════

# Connecteurs qui structurent l'argument
_CONNECT_OPPOSITION = {
    "mais","cependant","pourtant","néanmoins","toutefois","au contraire",
    "en revanche","malgré","bien que","quoique","alors que","tandis que",
    "certes","non pas","plutôt","au lieu","opposé",
}
_CONNECT_CAUSAL = {
    "car","parce que","puisque","donc","ainsi","c'est pourquoi","en effet",
    "de ce fait","par conséquent","d'où","il s'ensuit","grâce à",
    "à cause de","résulte","engendre","produit","permet","détermine",
}
_CONNECT_ILLUSTRATION = {
    "par exemple","notamment","ainsi","c'est-à-dire","autrement dit",
    "à savoir","tel que","comme","soit","soit encore",
}
_CONNECT_CONCLUSION = {
    "donc","ainsi","en conclusion","finalement","bref","en somme","d'où",
    "par conséquent","il en résulte","on peut donc","on voit que","ainsi",
}
_CONNECT_CONCESSION = {
    "certes","il est vrai","même si","bien que","on peut admettre","il faut reconnaître",
}
_CONNECT_THESE = {
    "j'affirme","je soutiens","je pense que","je crois que","à mon sens",
    "selon moi","il me semble","ma thèse","j'avance que","je propose",
}

# Marqueurs de modalité
_MODALITE = {
    "nécessité":  {"doit","faut","obligatoirement","nécessairement","inévitablement","forcément"},
    "possibilité":{"peut","pourrait","éventuellement","peut-être","possible","probablement","serait"},
    "certitude":  {"certainement","assurément","clairement","évidemment","bien sûr","indéniablement"},
    "doute":      {"peut-être","doute","incertain","hésiter","incertitude","supposer","hypothèse"},
    "négation":   {"ne","pas","non","jamais","rien","aucun","ni","nullement"},
}

# Verbes épistémiques (portent une proposition)
_VERBES_EPISTEMIQUES = {
    "être","avoir","faire","dire","penser","croire","savoir","vouloir","pouvoir",
    "devoir","affirmer","nier","montrer","démontrer","prouver","supposer",
    "postuler","définir","concevoir","considérer","estimer","reconnaître",
    "admettre","rejeter","contester","distinguer","opposer","comparer",
    "expliquer","analyser","qualifier","constituer","former","produire",
    "engendrer","causer","déterminer","conditionner","permettre","impliquer",
    "suggérer","indiquer","révéler","signifier","désigner","nommer",
    "identifier","représenter","symboliser","critiquer","réfuter","soutenir",
    "exister","vivre","percevoir","ressentir","comprendre","appréhender",
}

_PRONOMS_SUJETS = {
    "je","tu","il","elle","on","nous","vous","ils","elles","leia","ça","cela","ce",
}


def _normaliser(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "").strip().lower())


def _phrases(text: str) -> List[str]:
    """Découpage en phrases robuste (sans lib externe)."""
    # Protège les abréviations
    text = re.sub(r"\b(M|Mme|Mlle|Dr|Prof|etc|vol|p|pp|art|fig|cf|op|cit|ibid)\.", r"\1§", text)
    # Découpe sur . ! ? … suivi d'une majuscule
    parts = re.split(r"(?<=[.!?…])\s+(?=[A-ZÀÂÉÈÊËÎÏÔÙÛÜÇ\"\«])", text)
    return [p.replace("§", ".").strip() for p in parts if p.strip()]


class AnalyseurSyntaxique:
    """
    Analyse syntaxique heuristique du français — pure Python.
    Extraction SVO, structure de clause, connecteurs, modalité.
    """

    def __init__(self, morpho: FrenchMorphology):
        self.morpho = morpho

    def analyser_phrase(self, phrase: str) -> Dict[str, Any]:
        """Analyse syntaxique complète d'une phrase."""
        toks = self.morpho.tokenize(phrase)
        low = _normaliser(phrase)

        sujet    = self._sujet(toks, low)
        verbe    = self._verbe_principal(toks)
        objet    = self._objet(toks, verbe)
        negation = self._est_negatif(toks, low)
        modalite = self._modalite(toks, low)
        connecteur = self._connecteur(low)

        # Propositions enchâssées (relatives, subordonnées)
        enchassees = self._sous_clauses(phrase, toks)

        return {
            "sujet":      sujet,
            "verbe":      verbe,
            "objet":      objet,
            "negation":   negation,
            "modalite":   modalite,
            "connecteur": connecteur,
            "enchassees": enchassees,
            "tokens":     toks,
            "raw":        phrase,
        }

    def _sujet(self, toks: List[Dict], low: str) -> str:
        """Heuristique : pronom ou premier SN avant le verbe."""
        # Pronoms sujets
        for t in toks:
            if t["lemme"] in _PRONOMS_SUJETS:
                return t["lemme"]
        # Syntagme nominal avant un verbe
        verbe_idx = -1
        for i, t in enumerate(toks):
            if t["pos"] == "VERB":
                verbe_idx = i
                break
        if verbe_idx > 0:
            cands = [t for t in toks[:verbe_idx] if t["pos"] in ("NOUN","OTHER") and len(t["lemme"]) > 2]
            if cands:
                return cands[-1]["lemme"]
        return ""

    def _verbe_principal(self, toks: List[Dict]) -> str:
        """Identifie le verbe principal (ROOT)."""
        # Verbe conjugué : préférence pour les formes finies
        for t in toks:
            if t["pos"] == "VERB" and t["token"].lower() in _VERBES_IRREG:
                return _VERBES_IRREG[t["token"].lower()]
        for t in toks:
            if t["pos"] == "VERB":
                return t["lemme"]
        return ""

    def _objet(self, toks: List[Dict], verbe: str) -> str:
        """Premier SN après le verbe = objet probable."""
        verbe_vu = False
        for t in toks:
            if t["lemme"] == verbe:
                verbe_vu = True
                continue
            if verbe_vu and t["pos"] in ("NOUN","OTHER") and t["lemme"] not in _STOP:
                if len(t["lemme"]) > 2:
                    return t["lemme"]
        return ""

    def _est_negatif(self, toks: List[Dict], low: str) -> bool:
        """Détecte la négation : ne...pas, non, jamais, aucun."""
        neg_mots = {"ne","pas","non","jamais","rien","aucun","nullement","ni"}
        return any(t["lemme"] in neg_mots for t in toks)

    def _modalite(self, toks: List[Dict], low: str) -> str:
        """Détecte la modalité dominante."""
        scores: Dict[str, int] = Counter()
        lemmes = {t["lemme"] for t in toks}
        for mod, marqueurs in _MODALITE.items():
            for m in marqueurs:
                if m in lemmes or m in low:
                    scores[mod] += 1
        return scores.most_common(1)[0][0] if scores else "assertion"

    def _connecteur(self, low: str) -> str:
        """Détecte le type de connecteur logique."""
        for c in _CONNECT_OPPOSITION:
            if c in low:
                return "opposition"
        for c in _CONNECT_CAUSAL:
            if c in low:
                return "causal"
        for c in _CONNECT_CONCLUSION:
            if c in low:
                return "conclusion"
        for c in _CONNECT_ILLUSTRATION:
            if c in low:
                return "illustration"
        for c in _CONNECT_CONCESSION:
            if c in low:
                return "concession"
        for c in _CONNECT_THESE:
            if c in low:
                return "thèse"
        return ""

    def _sous_clauses(self, phrase: str, toks: List[Dict]) -> List[str]:
        """Détecte les sous-clauses relatives et complétives."""
        relatives = re.findall(r"(?:qui|que|dont|où)\s+(.{5,50}?)(?:[,;]|$)", phrase)
        completives = re.findall(r"(?:que|qu')\s+(.{5,60}?)(?:[,;.]|$)", phrase)
        return [r.strip() for r in (relatives + completives) if len(r.strip()) > 4][:4]

    def extraire_triplets(self, phrase: str) -> List[Dict[str, Any]]:
        """Extrait les triplets sémantiques (sujet, relation, objet) d'une phrase."""
        syn = self.analyser_phrase(phrase)
        triplets = []

        # Triplet principal
        if syn["sujet"] and syn["verbe"]:
            triplets.append({
                "sujet":    syn["sujet"],
                "relation": ("ne_" if syn["negation"] else "") + syn["verbe"],
                "objet":    syn["objet"] or "?",
                "negation": syn["negation"],
                "modalite": syn["modalite"],
                "connecteur": syn["connecteur"],
                "confiance": 0.8 if syn["sujet"] and syn["objet"] else 0.5,
                "source":   phrase[:80],
            })

        # Triplets des sous-clauses
        for sc in syn["enchassees"]:
            sub = self.analyser_phrase(sc)
            if sub["sujet"] and sub["verbe"]:
                triplets.append({
                    "sujet":    sub["sujet"],
                    "relation": sub["verbe"],
                    "objet":    sub["objet"] or "?",
                    "negation": sub["negation"],
                    "modalite": sub["modalite"],
                    "connecteur": "sous-clause",
                    "confiance": 0.55,
                    "source":   sc[:60],
                })

        # Pattern : "X est Y" / "X n'est pas Y"
        for m in re.finditer(
            r"([A-Za-zÀ-ÿ][a-zàâéèêëîïôùûüç\s\-]{2,30}?)\s+(n['e]?'?est pas|est|sont|devient)\s+"
            r"(?:un |une |des |le |la |les |l'|au )?"
            r"([a-zàâéèêëîïôùûüç\s\-]{3,35})",
            phrase, re.IGNORECASE
        ):
            neg = "pas" in m.group(2).lower()
            subj = _normaliser(m.group(1))
            obj  = _normaliser(m.group(3)).rstrip(" .,:;")
            if len(subj) > 2 and len(obj) > 2 and subj not in _STOP and obj not in _STOP:
                triplets.append({
                    "sujet":    subj[:40],
                    "relation": "ne_être" if neg else "être",
                    "objet":    obj[:40],
                    "negation": neg,
                    "modalite": "assertion",
                    "connecteur": syn["connecteur"],
                    "confiance": 0.85,
                    "source":   phrase[:80],
                })

        # Pattern : "selon X, Y"
        for m in re.finditer(
            r"(?:selon|d'après|pour|d'après)\s+([A-ZÀ-Ÿ][a-zàâéèêëîïôùûüç\s\-]{1,20}?),\s+(.{10,80})",
            phrase, re.IGNORECASE
        ):
            auteur = _normaliser(m.group(1))
            contenu = _normaliser(m.group(2))[:60]
            if len(auteur) > 2:
                triplets.append({
                    "sujet":    auteur,
                    "relation": "affirme",
                    "objet":    contenu,
                    "negation": False,
                    "modalite": "assertion",
                    "connecteur": "attribution",
                    "confiance": 0.75,
                    "source":   phrase[:80],
                })

        # Dédoublonner
        seen_keys: Set[str] = set()
        result = []
        for t in triplets:
            key = f"{t['sujet']}|{t['relation']}|{t['objet']}"
            if key not in seen_keys and len(t["sujet"]) > 1:
                seen_keys.add(key)
                result.append(t)
        return result


# ═══════════════════════════════════════════════════════════════════════════════
# III. GRAPHE CONCEPTUEL VIVANT
#      Ce graphe évolue à chaque appel — c'est la "mémoire vive" de Leia
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class NoeudConcept:
    """Un nœud vivant dans le graphe conceptuel de Leia."""
    label: str
    activation: float = 0.0       # 0 = dormant, 1 = pleinement actif
    ton_emotionnel: float = 0.0    # -1 négatif, 0 neutre, +1 positif
    familiarite: float = 0.0       # 0 = inconnu, 1 = très connu
    frequence: int = 0             # nb de fois rencontré
    derniere_activation: float = field(default_factory=time.time)
    premiere_vue: float = field(default_factory=time.time)
    surprenant: int = 0            # fois où ce concept était nouveau
    sources: List[str] = field(default_factory=list)  # d'où vient ce concept

    def decay(self, now: float, demi_vie: float = 3600.0) -> None:
        """Décroissance naturelle de l'activation avec le temps."""
        elapsed = now - self.derniere_activation
        factor = math.exp(-elapsed / demi_vie * math.log(2))
        self.activation = max(0.0, self.activation * factor)

    def activer(self, force: float, ton: float = 0.0, source: str = "") -> None:
        """Active ce concept avec une force donnée."""
        now = time.time()
        self.activation = min(1.0, self.activation + force)
        # Mise à jour du ton émotionnel (moyenne glissante)
        if ton != 0.0:
            alpha = 0.3
            self.ton_emotionnel = (1 - alpha) * self.ton_emotionnel + alpha * ton
        self.frequence += 1
        # Familiarité augmente logarithmiquement
        self.familiarite = min(1.0, math.log1p(self.frequence) / 6.0)
        self.derniere_activation = now
        if source and source not in self.sources:
            self.sources.append(source[:60])
            if len(self.sources) > 5:
                self.sources.pop(0)

    def est_nouveau(self) -> bool:
        return self.frequence <= 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "label": self.label,
            "activation": round(self.activation, 3),
            "ton_emotionnel": round(self.ton_emotionnel, 3),
            "familiarite": round(self.familiarite, 3),
            "frequence": self.frequence,
        }


@dataclass
class LienConceptuel:
    """Lien entre deux concepts dans le graphe."""
    source: str
    cible: str
    relation: str          # type de relation
    force: float = 0.5     # 0 faible, 1 fort
    direction: str = "→"   # "→" ou "↔" (bidirectionnel)
    contradictoire: bool = False
    créé_à: float = field(default_factory=time.time)

    def renforcer(self, delta: float = 0.1) -> None:
        self.force = min(1.0, self.force + delta)


class GrapheConceptuelVivant:
    """
    Graphe de concepts qui vit et évolue avec chaque texte/dialogue traité.
    C'est la "mémoire conceptuelle" de Leia — ce qu'elle a compris.
    """

    def __init__(self, demi_vie_heures: float = 2.0):
        self.noeuds: Dict[str, NoeudConcept] = {}
        self.liens: List[LienConceptuel] = []
        self._demi_vie = demi_vie_heures * 3600
        self._historique: deque = deque(maxlen=200)
        self._n_appels: int = 0

    # ── Accès aux nœuds ────────────────────────────────────────────────────

    def _noeud(self, label: str) -> NoeudConcept:
        if label not in self.noeuds:
            self.noeuds[label] = NoeudConcept(label=label)
        return self.noeuds[label]

    def _decay_all(self) -> None:
        now = time.time()
        for n in self.noeuds.values():
            n.decay(now, self._demi_vie)

    # ── Mise à jour du graphe ──────────────────────────────────────────────

    def integrer_concepts(self, concepts: List[str], source: str = "",
                          ton: float = 0.0) -> Dict[str, float]:
        """
        Intègre une liste de concepts dans le graphe.
        Retourne un dict label → résonance (0=nouveau, 1=très familier).
        """
        self._decay_all()
        self._n_appels += 1
        resonances: Dict[str, float] = {}

        for c in concepts:
            if not c or len(c) < 2:
                continue
            noeud = self._noeud(c)
            was_new = noeud.est_nouveau()
            force = 0.6 if was_new else 0.3
            noeud.activer(force, ton, source)
            if was_new:
                noeud.surprenant += 1
            resonances[c] = noeud.familiarite

        # Créer des liens entre co-concepts
        for i, a in enumerate(concepts):
            for b in concepts[i+1:i+4]:  # fenêtre de 3
                if a and b and a != b:
                    self._ajouter_lien(a, b, "co-occurrence", force=0.3)

        self._historique.append({
            "time": time.time(),
            "concepts": concepts[:10],
            "source": source[:40],
        })
        return resonances

    def integrer_triplet(self, sujet: str, relation: str, objet: str,
                         negation: bool = False, source: str = "") -> None:
        """Intègre un triplet dans le graphe sous forme de lien sémantique."""
        if not sujet or not objet:
            return
        self._noeud(sujet).activer(0.5, 0.0, source)
        self._noeud(objet).activer(0.4, 0.0, source)
        rel_label = f"{'¬' if negation else ''}{relation}"
        contradictoire = negation or relation.startswith("ne_")
        self._ajouter_lien(sujet, objet, rel_label,
                           force=0.6, contradictoire=contradictoire)

    def _ajouter_lien(self, src: str, tgt: str, relation: str,
                      force: float = 0.5, contradictoire: bool = False) -> None:
        """Ajoute ou renforce un lien entre deux concepts."""
        for lien in self.liens:
            if lien.source == src and lien.cible == tgt and lien.relation == relation:
                lien.renforcer(0.1)
                return
        self.liens.append(LienConceptuel(
            source=src, cible=tgt, relation=relation,
            force=force, contradictoire=contradictoire
        ))

    # ── Mesures vivantes ───────────────────────────────────────────────────

    def resonance(self, concepts: List[str]) -> float:
        """
        Mesure la résonance d'une liste de concepts avec le graphe existant.
        0 = tout est nouveau (pas de résonance)
        1 = tout est très familier et fortement connecté
        """
        if not concepts:
            return 0.0
        scores = []
        for c in concepts:
            if c in self.noeuds:
                n = self.noeuds[c]
                scores.append(n.familiarite * n.activation + n.familiarite * 0.5)
            else:
                scores.append(0.0)
        return min(1.0, sum(scores) / len(concepts))

    def surprise(self, concepts: List[str]) -> float:
        """
        Mesure la surprise : combien de ces concepts sont vraiment nouveaux.
        0 = rien de nouveau ; 1 = tout est nouveau
        """
        if not concepts:
            return 0.0
        nouveaux = sum(1 for c in concepts if c not in self.noeuds
                       or self.noeuds[c].frequence <= 1)
        return nouveaux / len(concepts)

    def tension(self, concepts: List[str]) -> float:
        """
        Mesure la tension conceptuelle : oppositions dans le graphe.
        """
        liens_contradictoires = [
            l for l in self.liens
            if l.contradictoire
            and (l.source in concepts or l.cible in concepts)
        ]
        return min(1.0, len(liens_contradictoires) * 0.25)

    def concepts_actifs(self, seuil: float = 0.2, n: int = 15) -> List[str]:
        """Retourne les N concepts actuellement les plus actifs."""
        actifs = [(label, n.activation) for label, n in self.noeuds.items()
                  if n.activation >= seuil]
        actifs.sort(key=lambda x: x[1], reverse=True)
        return [label for label, _ in actifs[:n]]

    def voisins(self, concept: str, n: int = 6) -> List[str]:
        """Concepts directement liés à un concept donné."""
        voisins = []
        for l in self.liens:
            if l.source == concept:
                voisins.append((l.cible, l.force))
            elif l.cible == concept:
                voisins.append((l.source, l.force))
        voisins.sort(key=lambda x: x[1], reverse=True)
        return [c for c, _ in voisins[:n]]

    def etat_interne(self) -> Dict[str, Any]:
        """Snapshot de l'état interne du graphe."""
        return {
            "n_concepts": len(self.noeuds),
            "n_liens": len(self.liens),
            "n_appels": self._n_appels,
            "concepts_actifs": self.concepts_actifs(seuil=0.3, n=10),
            "concepts_tres_familiers": [
                l for l, n in self.noeuds.items() if n.familiarite > 0.6
            ][:10],
        }

    def sauvegarder(self, path: str) -> None:
        """Sauvegarde le graphe en JSON."""
        data = {
            "noeuds": {l: n.to_dict() for l, n in self.noeuds.items()},
            "liens": [
                {"source": l.source, "cible": l.cible, "relation": l.relation,
                 "force": round(l.force, 3), "contradictoire": l.contradictoire}
                for l in self.liens
            ],
        }
        Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def charger(self, path: str) -> None:
        """Charge un graphe depuis JSON."""
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            for label, nd in data.get("noeuds", {}).items():
                n = self._noeud(label)
                n.activation = nd.get("activation", 0.0)
                n.ton_emotionnel = nd.get("ton_emotionnel", 0.0)
                n.familiarite = nd.get("familiarite", 0.0)
                n.frequence = nd.get("frequence", 0)
            for ld in data.get("liens", []):
                self.liens.append(LienConceptuel(
                    source=ld["source"], cible=ld["cible"],
                    relation=ld["relation"], force=ld.get("force", 0.5),
                    contradictoire=ld.get("contradictoire", False),
                ))
        except Exception:
            pass


# ═══════════════════════════════════════════════════════════════════════════════
# IV. DÉTECTEUR D'INTENTION — ce que la personne VEUT dire
# ═══════════════════════════════════════════════════════════════════════════════

_INTENTIONS = {
    "question_philosophique": [
        "est-ce que","qu'est-ce","pourquoi","comment peut","quel est le sens",
        "que signifie","qu'est","en quoi","dans quelle mesure","peut-on dire",
        "y a-t-il","faut-il","doit-on","est-il possible","comment expliquer",
    ],
    "question_directe": [
        "est-ce que","quel est","qui est","quand est","où est","combien",
        "quelle est","quels sont","quelles sont","comment est",
    ],
    "challenge": [
        "je ne suis pas d'accord","tu as tort","c'est faux","non tu","mais non",
        "pas d'accord","au contraire","je refuse","je conteste","c'est inexact",
        "tu te trompes","erreur","incorrect",
    ],
    "confidence_personnelle": [
        "je ressens","j'éprouve","j'ai peur","je souffre","j'aime","je hais",
        "ça me touche","je me sens","j'ai vécu","ma vie","mon expérience",
        "je vis","pour moi","à moi","ça me","il m'","je n'arrive",
    ],
    "expression_doute": [
        "je ne sais pas","peut-être","je doute","je ne suis pas sûr","hésiter",
        "incertain","bizarre","étrange","je me demande","curieux","tu crois",
    ],
    "demande_confirmation": [
        "non ?","n'est-ce pas","tu vois","pas vrai","tu comprends","c'est ça",
        "je me trompe","c'est bien ça","c'est juste",
    ],
    "affirmation_forte": [
        "j'affirme","je soutiens","c'est certain","absolument","clairement",
        "évidemment","bien sûr","indéniablement","c'est clair","forcément",
    ],
}

_POSTURES = {
    "certitude":   {"sûr","certain","certaine","clairement","évidemment","bien sûr","absolument","forcément"},
    "doute":       {"peut-être","doute","incertain","hésiter","incertitude","supposer","bizarre","je ne sais"},
    "scepticisme": {"pas d'accord","conteste","au contraire","mais","vraiment","pourtant"},
    "ouverture":   {"peut-être","intéressant","j'y pense","je découvre","question","explorer"},
}


class DetecteurIntention:
    """Détecte l'intention et la posture communicative d'un énoncé."""

    def intention(self, text: str) -> str:
        low = _normaliser(text)
        is_question = "?" in text

        for intent, marqueurs in _INTENTIONS.items():
            for m in marqueurs:
                if m in low:
                    if intent == "question_directe" and not is_question:
                        continue
                    return intent

        if is_question:
            return "question"
        return "affirmation"

    def posture(self, text: str) -> str:
        low = _normaliser(text)
        scores: Counter = Counter()
        for posture, marqueurs in _POSTURES.items():
            for m in marqueurs:
                if m in low:
                    scores[posture] += 1
        if scores:
            return scores.most_common(1)[0][0]
        return "neutre"

    def urgence(self, text: str) -> float:
        """Niveau d'urgence/intensité [0, 1]."""
        mots_urgents = {"urgent","aide","vite","maintenant","crise","problème",
                        "secours","immédiatement","important","grave","critique"}
        low = _normaliser(text)
        score = (
            ("!" in text) * 0.3 +
            text.count("!") * 0.1 +
            sum(0.2 for m in mots_urgents if m in low)
        )
        return min(1.0, score)

    def argument_type(self, text: str) -> str:
        """Détecte le type argumentatif d'une phrase."""
        low = _normaliser(text)
        for c in _CONNECT_THESE:
            if c in low:
                return "thèse"
        for c in _CONNECT_CONCESSION:
            if c in low:
                return "concession"
        for c in _CONNECT_OPPOSITION:
            if c in low:
                return "objection"
        for c in _CONNECT_CONCLUSION:
            if c in low:
                return "conclusion"
        for c in _CONNECT_ILLUSTRATION:
            if c in low:
                return "illustration"
        return ""


# ═══════════════════════════════════════════════════════════════════════════════
# V. SEGMENTATION ET COMPRÉHENSION DE TEXTE LONG
# ═══════════════════════════════════════════════════════════════════════════════

class SegmenteurThematique:
    """
    Découpe un texte long en blocs thématiques cohérents.
    Détecte les ruptures thématiques par changement de vocabulaire.
    """

    def __init__(self, morpho: FrenchMorphology):
        self.morpho = morpho

    def segmenter(self, text: str, taille_cible: int = 400) -> List[Dict[str, Any]]:
        """
        Découpe le texte en segments thématiques.
        Chaque segment contient : texte, concepts, type_argumentatif.
        """
        phrases = _phrases(text)
        if not phrases:
            return [{"texte": text[:400], "concepts": [], "arg_type": ""}]

        segments = []
        curseur = 0
        bloc_courant: List[str] = []
        taille_courante = 0

        detecteur = DetecteurIntention()

        for ph in phrases:
            bloc_courant.append(ph)
            taille_courante += len(ph)

            # Rupture thématique ou taille atteinte
            if taille_courante >= taille_cible or self._rupture(bloc_courant):
                bloc_txt = " ".join(bloc_courant)
                concepts = self.morpho.content_words(bloc_txt)[:15]
                freq = Counter(concepts)
                concepts_tri = [w for w, _ in freq.most_common(10) if len(w) > 3]
                arg_type = detecteur.argument_type(bloc_txt)

                segments.append({
                    "texte":    bloc_txt[:500],
                    "concepts": concepts_tri,
                    "arg_type": arg_type,
                    "position": curseur,
                })
                curseur += len(bloc_courant)
                bloc_courant = []
                taille_courante = 0

        # Dernier bloc
        if bloc_courant:
            bloc_txt = " ".join(bloc_courant)
            concepts = [w for w, _ in Counter(
                self.morpho.content_words(bloc_txt)
            ).most_common(10) if len(w) > 3]
            segments.append({
                "texte":    bloc_txt[:500],
                "concepts": concepts,
                "arg_type": detecteur.argument_type(bloc_txt),
                "position": curseur,
            })

        return segments if segments else [{"texte": text[:400], "concepts": [], "arg_type": ""}]

    def _rupture(self, bloc: List[str]) -> bool:
        """Détecte une rupture thématique (connecteur fort de transition)."""
        if len(bloc) < 2:
            return False
        derniere = _normaliser(bloc[-1])
        transitions = {"premièrement","deuxièmement","troisièmement","ensuite",
                       "enfin","pour conclure","en résumé","par ailleurs",
                       "d'autre part","d'un côté","d'un autre","en premier lieu"}
        return any(t in derniere for t in transitions)


# ═══════════════════════════════════════════════════════════════════════════════
# VI. MESURE DE COHÉRENCE — Leia s'entend penser
# ═══════════════════════════════════════════════════════════════════════════════

class MesureurCoherence:
    """
    Mesure la cohérence entre une réponse et les concepts actifs de Leia.
    Utilisé par self_monitoring_filter pour éviter les réponses vides.
    100% pure Python — TF-IDF maison.
    """

    def __init__(self):
        self._idf: Dict[str, float] = {}
        self._df: Dict[str, int] = {}
        self._n_docs: int = 0

    def apprendre(self, text: str) -> None:
        """Met à jour le vocabulaire IDF avec un nouveau texte."""
        mots = set(re.findall(r"[a-zA-ZÀ-ÿ]{3,}", text.lower()))
        self._n_docs += 1
        for m in mots:
            self._df[m] = self._df.get(m, 0) + 1
        # Recalcule IDF
        N = max(self._n_docs, 1)
        self._idf = {
            w: math.log((N + 1) / (df + 1)) + 1.0
            for w, df in self._df.items()
        }

    def vecteur(self, text: str) -> Dict[str, float]:
        """Vecteur TF-IDF d'un texte."""
        mots = re.findall(r"[a-zA-ZÀ-ÿ]{3,}", text.lower())
        mots = [m for m in mots if m not in _STOP]
        if not mots:
            return {}
        tf = Counter(mots)
        total = len(mots)
        return {w: (cnt / total) * self._idf.get(w, 1.0) for w, cnt in tf.items()}

    def similarite(self, text_a: str, text_b: str) -> float:
        """Similarité cosinus TF-IDF entre deux textes [0, 1]."""
        va = self.vecteur(text_a)
        vb = self.vecteur(text_b)
        if not va or not vb:
            return self._jaccard(text_a, text_b)
        num = sum(va.get(w, 0.0) * vb.get(w, 0.0) for w in va if w in vb)
        den = math.sqrt(sum(v**2 for v in va.values())) * math.sqrt(sum(v**2 for v in vb.values()))
        return min(1.0, num / den) if den > 0 else 0.0

    def _jaccard(self, a: str, b: str) -> float:
        sa = set(re.findall(r"[a-zA-ZÀ-ÿ]{3,}", a.lower())) - _STOP
        sb = set(re.findall(r"[a-zA-ZÀ-ÿ]{3,}", b.lower())) - _STOP
        if not sa or not sb:
            return 0.0
        return len(sa & sb) / len(sa | sb)

    def est_coherente(self, reponse: str, concepts_actifs: List[str],
                      seuil: float = 0.12) -> bool:
        """Vérifie si une réponse reflète les concepts actifs."""
        if not concepts_actifs:
            return True
        mots_rep = set(re.findall(r"[a-zA-ZÀ-ÿ]{3,}", reponse.lower())) - _STOP
        inter = mots_rep & set(concepts_actifs)
        return len(inter) / max(len(concepts_actifs), 1) >= seuil

    def contient_meta(self, texte: str) -> bool:
        """Détecte les fuites de métadonnées internes (noms de modules, etc.)."""
        _META = {
            "pressure","payload","metadata","filename","debug","snapshot",
            "pipeline","module","neurone","json","python","score","weight",
            "valence","engine","weaver","label","token","field","source",
        }
        low = texte.lower()
        if "_" in texte or re.search(r"[{}\[\]<>]", texte):
            return True
        return any(re.search(rf"\b{m}\b", low) for m in _META)


# ═══════════════════════════════════════════════════════════════════════════════
# VII. RÉSULTATS DE COMPRÉHENSION — dataclasses de sortie
# ═══════════════════════════════════════════════════════════════════════════════

@dataclass
class ComprehensionDialogue:
    """
    Ce que Leia a compris d'un message utilisateur.
    Produit par LeiaComprehensionVivante.dialogue().
    """
    # Intention et posture
    intention: str = ""           # "question_philosophique", "challenge", ...
    posture: str = ""             # "certitude", "doute", "neutre", ...
    modalite: str = ""            # "assertion", "possibilité", "nécessité", ...

    # Structure grammaticale
    sujet_grammatical: str = ""
    verbe_principal: str = ""
    objet_grammatical: str = ""
    est_question: bool = False
    est_negatif: bool = False
    est_personnel: bool = False

    # Contenu conceptuel
    concepts_focaux: List[str] = field(default_factory=list)
    mots_contenu: List[str] = field(default_factory=list)
    triplets: List[Dict[str, Any]] = field(default_factory=list)

    # État vivant — ce que ça produit en Leia
    resonance: float = 0.0        # 0 = rien de familier | 1 = très résonnant
    surprise: float = 0.0         # 0 = tout est connu | 1 = tout est nouveau
    tension: float = 0.0          # 0 = pas de conflit | 1 = opposition forte
    charge_emotionnelle: float = 0.0   # -1 négatif | +1 positif
    urgence: float = 0.0

    # Concepts proches dans le graphe interne
    concepts_actives: List[str] = field(default_factory=list)
    voisins_graphe: List[str] = field(default_factory=list)

    # Méta
    n_mots: int = 0
    raw: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "intention": self.intention,
            "posture": self.posture,
            "modalite": self.modalite,
            "sujet": self.sujet_grammatical,
            "verbe": self.verbe_principal,
            "objet": self.objet_grammatical,
            "est_question": self.est_question,
            "est_negatif": self.est_negatif,
            "est_personnel": self.est_personnel,
            "concepts_focaux": self.concepts_focaux[:8],
            "mots_contenu": self.mots_contenu[:12],
            "triplets": self.triplets[:5],
            "resonance": round(self.resonance, 3),
            "surprise": round(self.surprise, 3),
            "tension": round(self.tension, 3),
            "charge_emotionnelle": round(self.charge_emotionnelle, 3),
            "urgence": round(self.urgence, 3),
            "concepts_actives": self.concepts_actives[:8],
            "voisins_graphe": self.voisins_graphe[:6],
            "n_mots": self.n_mots,
        }


@dataclass
class ComprehensionTexte:
    """
    Ce que Leia a compris d'un texte lu (livre, PDF, passage).
    Produit par LeiaComprehensionVivante.texte().
    """
    # Vue globale
    concepts_cles: List[str] = field(default_factory=list)
    triplets: List[Dict[str, Any]] = field(default_factory=list)
    themes: List[str] = field(default_factory=list)

    # Structure argumentative
    theses: List[str] = field(default_factory=list)
    objections: List[str] = field(default_factory=list)
    concessions: List[str] = field(default_factory=list)
    conclusions: List[str] = field(default_factory=list)

    # Segments thématiques
    segments: List[Dict[str, Any]] = field(default_factory=list)

    # Ce que ça produit en Leia
    resonance: float = 0.0        # liens avec ce qu'elle sait déjà
    surprise: float = 0.0         # ce qui est vraiment nouveau
    tension: float = 0.0          # oppositions internes au texte
    charge_emotionnelle: float = 0.0

    # Entités repérées (noms propres, auteurs, lieux)
    entites: List[Dict[str, str]] = field(default_factory=list)

    # Modalité dominante
    modalite_dominante: str = ""
    densite_lexicale: float = 0.0

    # Méta
    n_phrases: int = 0
    n_mots: int = 0
    source: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "concepts_cles": self.concepts_cles[:20],
            "triplets": self.triplets[:15],
            "themes": self.themes[:8],
            "theses": self.theses[:4],
            "objections": self.objections[:4],
            "conclusions": self.conclusions[:3],
            "segments": len(self.segments),
            "resonance": round(self.resonance, 3),
            "surprise": round(self.surprise, 3),
            "tension": round(self.tension, 3),
            "charge_emotionnelle": round(self.charge_emotionnelle, 3),
            "entites": self.entites[:10],
            "modalite_dominante": self.modalite_dominante,
            "densite_lexicale": round(self.densite_lexicale, 3),
            "n_phrases": self.n_phrases,
            "n_mots": self.n_mots,
            "source": self.source,
        }


# ═══════════════════════════════════════════════════════════════════════════════
# VIII. MOTEUR DE COMPRÉHENSION VIVANTE — point d'entrée unique
# ═══════════════════════════════════════════════════════════════════════════════

class LeiaComprehensionVivante:
    """
    Moteur de compréhension vivante de Leia.
    Pure Python — zéro dépendance externe.

    Ce moteur comprend réellement ce que l'utilisateur dit et ce qu'il lit,
    en maintenant un graphe conceptuel vivant qui évolue à chaque appel.

    Usage :
        from leia_comprehension_vivante import comprendre

        r = comprendre.dialogue("Est-ce que la liberté peut exister sans contrainte ?")
        r2 = comprendre.texte(passage_livre, source="Bergson")
    """

    def __init__(self, chemin_persistance: Optional[str] = None):
        self.morpho     = FrenchMorphology()
        self.syntaxe    = AnalyseurSyntaxique(self.morpho)
        self.graphe     = GrapheConceptuelVivant()
        self.intention  = DetecteurIntention()
        self.segment    = SegmenteurThematique(self.morpho)
        self.coherence  = MesureurCoherence()

        self._chemin    = chemin_persistance
        self._n_dialogues = 0
        self._n_textes    = 0
        self._hist_concepts: deque = deque(maxlen=50)

        if chemin_persistance:
            self.charger(chemin_persistance)

    # ── Compréhension de dialogue ──────────────────────────────────────────

    def dialogue(self, texte: str) -> ComprehensionDialogue:
        """
        Comprend réellement ce que l'utilisateur dit.

        Analyse complète : intention, posture, structure grammaticale,
        concepts, triplets sémantiques + état vivant (résonance, surprise, tension).
        """
        if not texte or not texte.strip():
            return ComprehensionDialogue(raw=texte or "")

        self._n_dialogues += 1

        # 1. Analyse syntaxique de la (ou des) phrase(s)
        phrases = _phrases(texte) or [texte]
        all_triplets: List[Dict] = []
        for ph in phrases:
            all_triplets.extend(self.syntaxe.extraire_triplets(ph))

        # Analyse de la phrase principale
        syn_principal = self.syntaxe.analyser_phrase(phrases[0])

        # 2. Contenu conceptuel
        mots = self.morpho.content_words(texte)
        freq = Counter(mots)
        # Focus = mots les plus importants (longs + fréquents)
        focaux = sorted(set(mots), key=lambda w: freq[w] * math.log(len(w) + 1), reverse=True)
        focaux = [w for w in focaux if len(w) > 3 and w not in _STOP][:10]

        # 3. Intention et posture
        intent = self.intention.intention(texte)
        posture = self.intention.posture(texte)
        urgence = self.intention.urgence(texte)

        # 4. Entités nommées (heuristique)
        # Majuscules en milieu de phrase = probablement nom propre ou concept clé
        entites_mots = re.findall(
            r"(?<![.!?]\s)(?<!\n)([A-ZÀÂÉÈÊËÎÏÔÙÛÜÇ][a-zàâéèêëîïôùûüç]+(?:\s[A-ZÀÂÉÈÊËÎÏÔÙÛÜÇ][a-zàâéèêëîïôùûüç]+)*)",
            texte[2:]  # Ignore le premier mot (début de phrase)
        )
        entites_mots = list(dict.fromkeys(entites_mots))[:6]

        # 5. Mise à jour du graphe vivant
        tous_concepts = focaux + [w for w in entites_mots if w.lower() not in _STOP]
        ton = self.morpho.valence(texte)
        self.graphe.integrer_concepts(tous_concepts, source=f"dialogue_{self._n_dialogues}", ton=ton)
        for t in all_triplets:
            self.graphe.integrer_triplet(t["sujet"], t["relation"], t["objet"],
                                         t["negation"], texte[:40])

        # 6. Mesures vivantes
        res   = self.graphe.resonance(focaux)
        surp  = self.graphe.surprise(focaux)
        tens  = self.graphe.tension(focaux)

        # 7. Cohérence (apprentissage IDF)
        self.coherence.apprendre(texte)
        self._hist_concepts.extend(focaux)

        # 8. Voisins dans le graphe (ce que ça active d'autre)
        voisins = []
        for c in focaux[:3]:
            voisins.extend(self.graphe.voisins(c, n=3))
        voisins = list(dict.fromkeys(v for v in voisins if v not in focaux))[:6]

        return ComprehensionDialogue(
            intention=intent,
            posture=posture,
            modalite=syn_principal["modalite"],
            sujet_grammatical=syn_principal["sujet"],
            verbe_principal=syn_principal["verbe"],
            objet_grammatical=syn_principal["objet"],
            est_question="?" in texte or intent.startswith("question"),
            est_negatif=syn_principal["negation"],
            est_personnel=bool(re.search(r"\b(je|mon|ma|mes|moi|j')\b", texte.lower())),
            concepts_focaux=focaux,
            mots_contenu=mots[:20],
            triplets=all_triplets[:8],
            resonance=res,
            surprise=surp,
            tension=tens,
            charge_emotionnelle=ton,
            urgence=urgence,
            concepts_actives=self.graphe.concepts_actifs(seuil=0.25, n=10),
            voisins_graphe=voisins,
            n_mots=len(texte.split()),
            raw=texte,
        )

    # ── Compréhension de texte lu ──────────────────────────────────────────

    def texte(self, texte: str, source: str = "",
              max_chars: int = 80_000) -> ComprehensionTexte:
        """
        Comprend réellement un texte lu (livre, PDF, passage).

        Construit une compréhension profonde :
        - Concepts clés + structure argumentative + triplets sémantiques
        - Mise à jour du graphe vivant (Leia "apprend" en lisant)
        - Mesures : résonance, surprise, tension, charge émotionnelle
        """
        if not texte or not texte.strip():
            return ComprehensionTexte(source=source)

        texte = texte[:max_chars]
        self._n_textes += 1

        # 1. Segmentation thématique
        segments = self.segment.segmenter(texte, taille_cible=500)

        # 2. Analyse phrase par phrase
        phrases = _phrases(texte)
        all_triplets: List[Dict] = []
        freq_globale: Counter = Counter()
        theses, objections, concessions, conclusions = [], [], [], []
        modalites: Counter = Counter()

        for ph in phrases:
            if len(ph) < 8:
                continue
            # Triplets
            triplets_ph = self.syntaxe.extraire_triplets(ph)
            all_triplets.extend(triplets_ph)
            # Concepts
            mots = self.morpho.content_words(ph)
            freq_globale.update(mots)
            # Structure argumentative
            low = _normaliser(ph)
            arg = self.intention.argument_type(ph)
            if arg == "thèse" and len(ph) > 20:
                theses.append(ph[:150])
            elif arg == "objection":
                objections.append(ph[:150])
            elif arg == "concession":
                concessions.append(ph[:150])
            elif arg == "conclusion":
                conclusions.append(ph[:150])
            # Modalité
            modalite = self.syntaxe.analyser_phrase(ph)["modalite"]
            modalites[modalite] += 1

        # 3. Concepts clés (saillance = fréquence × longueur)
        concepts_cles = [
            w for w, cnt in freq_globale.most_common(50)
            if len(w) > 3 and w not in _STOP and cnt >= 1
        ][:25]

        # 4. Thèmes (bigrams co-fréquents)
        themes = self._extraire_themes(texte, concepts_cles)

        # 5. Entités nommées
        entites = self._entites(texte)

        # 6. Mise à jour du graphe vivant
        ton = self.morpho.valence(texte)
        self.graphe.integrer_concepts(
            concepts_cles[:20], source=f"texte_{source[:20]}", ton=ton
        )
        for t in all_triplets:
            self.graphe.integrer_triplet(
                t["sujet"], t["relation"], t["objet"],
                t["negation"], source[:40]
            )

        # 7. Mesures vivantes
        res  = self.graphe.resonance(concepts_cles[:12])
        surp = self.graphe.surprise(concepts_cles[:12])
        tens = self.graphe.tension(concepts_cles[:12])

        # 8. Cohérence IDF
        self.coherence.apprendre(texte)

        # 9. Densité lexicale
        total_mots = len(re.findall(r"[a-zA-ZÀ-ÿ]{2,}", texte))
        mots_plein = sum(freq_globale.values())
        densite = mots_plein / max(total_mots, 1)

        # Modalité dominante
        modalite_dom = modalites.most_common(1)[0][0] if modalites else "assertion"

        return ComprehensionTexte(
            concepts_cles=concepts_cles,
            triplets=all_triplets[:30],
            themes=themes,
            theses=list(dict.fromkeys(theses))[:5],
            objections=list(dict.fromkeys(objections))[:5],
            concessions=list(dict.fromkeys(concessions))[:3],
            conclusions=list(dict.fromkeys(conclusions))[:4],
            segments=segments,
            resonance=res,
            surprise=surp,
            tension=tens,
            charge_emotionnelle=ton,
            entites=entites,
            modalite_dominante=modalite_dom,
            densite_lexicale=round(densite, 3),
            n_phrases=len(phrases),
            n_mots=total_mots,
            source=source,
        )

    # ── Utilitaires ────────────────────────────────────────────────────────

    def similarite(self, a: str, b: str) -> float:
        """Similarité sémantique entre deux textes [0, 1] — TF-IDF cosinus."""
        self.coherence.apprendre(a)
        self.coherence.apprendre(b)
        return self.coherence.similarite(a, b)

    def est_coherente(self, reponse: str) -> bool:
        """Vérifie que la réponse de Leia est cohérente avec ses concepts actifs."""
        actifs = self.graphe.concepts_actifs(seuil=0.2, n=12)
        return self.coherence.est_coherente(reponse, actifs)

    def etat_vivant(self) -> Dict[str, Any]:
        """Snapshot de l'état interne vivant de Leia."""
        return {
            "graphe": self.graphe.etat_interne(),
            "n_dialogues": self._n_dialogues,
            "n_textes": self._n_textes,
            "concepts_recents": list(self._hist_concepts)[-10:],
        }

    def sauvegarder(self, chemin: Optional[str] = None) -> None:
        path = chemin or self._chemin
        if path:
            self.graphe.sauvegarder(path)

    def charger(self, chemin: str) -> None:
        if Path(chemin).exists():
            self.graphe.charger(chemin)

    def _extraire_themes(self, texte: str, concepts: List[str]) -> List[str]:
        """Construit des thèmes depuis les bigrams de concepts co-fréquents."""
        phrases = _phrases(texte)
        cooc: Counter = Counter()
        top = set(concepts[:15])
        for ph in phrases:
            mots_ph = set(self.morpho.content_words(ph))
            dans_ph = top & mots_ph
            dans_ph_list = sorted(dans_ph)
            for i, a in enumerate(dans_ph_list):
                for b in dans_ph_list[i+1:i+3]:
                    cooc[(a, b)] += 1
        themes = [f"{a} / {b}" for (a, b), cnt in cooc.most_common(8) if cnt >= 2]
        # Compléter avec concepts seuls si peu de bigrams
        if len(themes) < 4:
            themes += [c for c in concepts[:8] if c not in " ".join(themes)]
        return list(dict.fromkeys(themes))[:10]

    def _entites(self, texte: str) -> List[Dict[str, str]]:
        """Extraction heuristique d'entités nommées."""
        entites = []
        seen: Set[str] = set()

        # Philosophes et auteurs classiques
        _AUTEURS = {
            "bergson","kant","hegel","descartes","nietzsche","platon","aristote",
            "spinoza","sartre","heidegger","wittgenstein","foucault","deleuze",
            "derrida","leibniz","locke","hume","rousseau","voltaire","pascal",
            "montaigne","merleau-ponty","husserl","freud","lacan","marx","weber",
            "durkheim","tocqueville","camus","beauvoir","arendt","rawls",
        }
        low = texte.lower()
        for auteur in _AUTEURS:
            if auteur in low and auteur not in seen:
                seen.add(auteur)
                ctx = ""
                idx = low.find(auteur)
                if idx >= 0:
                    ctx = texte[max(0, idx-15):idx+len(auteur)+25].strip()
                entites.append({"texte": auteur.title(), "type": "PERSONNE", "contexte": ctx})

        # Noms propres (capitalisés en milieu de phrase)
        for m in re.finditer(
            r"(?<=[.!?,;]\s)([A-ZÀÂÉÈÊËÎÏÔÙÛÜÇ][a-zàâéèêëîïôùûüç]+(?:\s[A-ZÀÂÉÈÊËÎÏÔÙÛÜÇ][a-zàâéèêëîïôùûüç]+)*)",
            texte
        ):
            nom = m.group(1)
            if (len(nom) > 3 and nom.lower() not in _STOP
                    and nom.lower() not in seen):
                seen.add(nom.lower())
                entites.append({"texte": nom, "type": "PROPRE", "contexte": ""})

        return entites[:20]


# ═══════════════════════════════════════════════════════════════════════════════
# INSTANCE GLOBALE — partagée par tous les modules Leia
# ═══════════════════════════════════════════════════════════════════════════════

comprendre = LeiaComprehensionVivante()
"""
Instance globale de Leia — partagée par tous les modules.

Import dans chaque module :
    from leia_comprehension_vivante import comprendre

    r = comprendre.dialogue(texte_utilisateur)
    r2 = comprendre.texte(passage_livre, source="Bergson")
"""


# ═══════════════════════════════════════════════════════════════════════════════
# DIAGNOSTIC EN LIGNE DE COMMANDE
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":

    def ligne(titre=""):
        print(f"\n{'─'*62}")
        if titre:
            print(f"  {titre}")
            print(f"{'─'*62}")

    print("═"*62)
    print("  LEIA — Moteur de Compréhension Vivante")
    print("  Pure Python · Zéro dépendance · Vivant")
    print("═"*62)

    # ── Test Dialogue ──────────────────────────────────────────────────
    ligne("TEST DIALOGUE")
    tests_dialogue = [
        "Est-ce que la liberté peut vraiment exister sans contrainte ?",
        "Je ne suis pas d'accord — la mémoire n'est pas un simple tiroir.",
        "Bergson affirme que la durée est irréductible à l'espace géométrique.",
        "J'ai peur que l'intelligence artificielle efface quelque chose d'essentiel en nous.",
        "Pourquoi la conscience est-elle si difficile à définir ?",
    ]
    for msg in tests_dialogue:
        r = comprendre.dialogue(msg)
        print(f"\n  ▶ {msg[:65]}")
        print(f"    intention   : {r.intention}")
        print(f"    posture     : {r.posture} | modalité : {r.modalite}")
        print(f"    focus       : {r.concepts_focaux[:5]}")
        print(f"    SVO         : ({r.sujet_grammatical!r}, {r.verbe_principal!r}, {r.objet_grammatical!r})")
        print(f"    triplets    : {len(r.triplets)}")
        for t in r.triplets[:2]:
            neg = "¬" if t.get("negation") else ""
            print(f"      → ({t['sujet']}, {neg}{t['relation']}, {t['objet']})")
        print(f"    résonance   : {r.resonance:.3f} | surprise : {r.surprise:.3f} | tension : {r.tension:.3f}")
        print(f"    émotion     : {r.charge_emotionnelle:+.3f} | urgence : {r.urgence:.2f}")
        print(f"    voisins     : {r.voisins_graphe[:4]}")

    # ── Test Texte / Livre ─────────────────────────────────────────────
    ligne("TEST LECTURE TEXTE (Bergson)")
    passage = (
        "La mémoire, selon Bergson, n'est pas un tiroir où l'on range des souvenirs isolés. "
        "Elle est une durée vécue, une continuité vivante qui déborde la perception immédiate. "
        "Certes, on peut admettre que certains souvenirs prennent une forme fixe dans le cerveau. "
        "Mais Bergson soutient que cette image figée trahit l'essence même du souvenir, "
        "qui est mouvement, passage, flux irréductible à l'espace. "
        "Locke, au contraire, considère que la mémoire est fondée sur des impressions passées, "
        "des traces fixes qui permettent de reconnaître les idées déjà éprouvées. "
        "Cette opposition révèle deux conceptions du temps : le temps mesuré et le temps vécu. "
        "On peut donc affirmer que la question de la mémoire engage nécessairement "
        "une philosophie du temps et de la conscience, et non seulement de la neurologie. "
        "Car comprendre la mémoire, c'est comprendre comment le passé continue à vivre dans le présent."
    )
    rt = comprendre.texte(passage, source="Bergson - Matière et Mémoire")
    print(f"\n  Source : {rt.source}")
    print(f"  Phrases : {rt.n_phrases} | Mots : {rt.n_mots} | Densité lexicale : {rt.densite_lexicale:.2f}")
    print(f"\n  Concepts clés  : {rt.concepts_cles[:10]}")
    print(f"  Thèmes         : {rt.themes[:5]}")
    print(f"  Entités        : {[e['texte'] for e in rt.entites[:6]]}")
    print(f"\n  Triplets ({len(rt.triplets)}) :")
    for t in rt.triplets[:5]:
        neg = "¬" if t.get("negation") else ""
        print(f"    ({t['sujet']}, {neg}{t['relation']}, {t['objet']}) [{t['connecteur'] or '—'}]")
    print(f"\n  Thèses     : {rt.theses[:2]}")
    print(f"  Objections : {rt.objections[:2]}")
    print(f"  Conclusions: {rt.conclusions[:2]}")
    print(f"\n  Résonance  : {rt.resonance:.3f}")
    print(f"  Surprise   : {rt.surprise:.3f}")
    print(f"  Tension    : {rt.tension:.3f}")
    print(f"  Émotion    : {rt.charge_emotionnelle:+.3f}")
    print(f"  Modalité   : {rt.modalite_dominante}")

    # ── Test Graphe Vivant ─────────────────────────────────────────────
    ligne("ÉTAT VIVANT DU GRAPHE")
    etat = comprendre.etat_vivant()
    print(f"\n  Concepts dans le graphe  : {etat['graphe']['n_concepts']}")
    print(f"  Liens dans le graphe     : {etat['graphe']['n_liens']}")
    print(f"  Dialogues traités        : {etat['n_dialogues']}")
    print(f"  Textes traités           : {etat['n_textes']}")
    print(f"  Concepts actuellement actifs : {etat['graphe']['concepts_actifs'][:8]}")
    print(f"  Concepts très familiers      : {etat['graphe']['concepts_tres_familiers'][:8]}")

    # ── Test Similarité ────────────────────────────────────────────────
    ligne("TEST SIMILARITÉ SÉMANTIQUE")
    paires = [
        ("La liberté est une valeur essentielle.", "La liberté suppose un choix réel."),
        ("La mémoire est une durée vécue.", "L'oubli est une forme de liberté."),
        ("Le chat dort sur le canapé.", "La philosophie du temps chez Bergson."),
    ]
    for a, b in paires:
        score = comprendre.similarite(a, b)
        print(f"  {score:.3f}  |  '{a[:38]}' ↔ '{b[:38]}'")

    # ── Test Cohérence ─────────────────────────────────────────────────
    ligne("TEST COHÉRENCE DE RÉPONSE")
    reponses = [
        "La mémoire selon Bergson est une durée, pas un stockage.",
        "Bonjour, comment allez-vous aujourd'hui ?",
        "Le temps vécu et la conscience sont au cœur de cette question.",
    ]
    for rep in reponses:
        ok = comprendre.est_coherente(rep)
        print(f"  {'✓' if ok else '✗'}  {rep[:55]}")

    print("\n" + "═"*62)
    print("  Aucune dépendance externe. Python pur.")
    print("═"*62 + "\n")
