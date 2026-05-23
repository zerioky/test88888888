"""concept_relation_engine.py — compréhension non-LLM par relations conceptuelles.

But : transformer une lecture en graphe de relations utilisables par Leia.
Ce module ne génère aucune phrase conversationnelle. Il extrait, stocke et
réactive seulement des triplets conceptuels : sujet --relation--> objet.

Priorité : zéro LLM, zéro réponse préécrite, extraction locale.
- Si spaCy + modèle français sont disponibles, on utilise les dépendances.
- Sinon, un extracteur regex français prend le relais pour rester fonctionnel.
"""
from __future__ import annotations

import json
import os
import re
import time
import unicodedata
from collections import Counter, defaultdict
from typing import Any, Dict, Iterable, List, Mapping, Optional, Tuple


def _strip_accents(text: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')


def _norm(text: Any) -> str:
    s = str(text or '').lower().replace('_', ' ')
    s = re.sub(r"[^a-zà-ÿ0-9'\-\s]", ' ', s)
    s = re.sub(r'\s+', ' ', s).strip(" -'\t\n\r")
    return s


def _public_concept(text: Any, *, max_words: int = 5) -> str:
    s = _norm(text)
    if not s:
        return ''
    # Stop pollution : noms de fichiers, variables internes, labels de code.
    banned_fragments = (
        '.pdf', '.txt', '.py', 'filename', 'metadata', 'payload', 'context',
        'pressure', 'auditif', 'auditory', 'signal', 'label', 'storage path',
        'henri bergson matière', 'henri bergson matiere',
    )
    no_acc = _strip_accents(s)
    if any(_strip_accents(b) in no_acc for b in banned_fragments):
        return ''
    if '_' in str(text or ''):
        return ''
    words = [w for w in s.split() if len(w) > 1]
    stop = {
        'le','la','les','un','une','des','du','de','d','ce','cet','cette','ces','son','sa','ses',
        'mon','ma','mes','ton','ta','tes','notre','votre','leur','leurs','qui','que','quoi','dont',
        'pour','par','dans','sur','avec','sans','vers','comme','plus','moins','très','tres',
        'est','sont','être','etre','été','ete','fait','font','peut','peuvent','doit','doivent',
        'il','elle','on','nous','vous','ils','elles','je','tu','me','te','se','y','en',
    }
    while words and words[0] in stop:
        words.pop(0)
    while words and words[-1] in stop:
        words.pop()
    words = words[:max_words]
    s = ' '.join(words)
    return s if len(s) >= 3 else ''


class ConceptRelationEngine:
    """Graphe conceptuel local, non génératif.

    Les relations sont stockées avec : source, relation, target, evidence,
    confidence, source_doc, created_at. Le moteur peut ensuite réactiver les
    relations pertinentes pour une question utilisateur.
    """

    RELATION_ALIASES = {
        'est': 'est', 'sont': 'est', 'être': 'est', 'etre': 'est', 'devient': 'devient',
        'signifie': 'signifie', 'contient': 'contient', 'comprend': 'contient',
        'porte': 'contient', 'garde': 'contient', 'reçoit': 'reçoit', 'recoit': 'reçoit',
        'produit': 'produit', 'cause': 'cause', 'précède': 'précède', 'precede': 'précède',
        'suit': 'suit', 'dépend': 'dépend_de', 'depend': 'dépend_de', 'résiste': 'résiste_à',
        'resiste': 'résiste_à', 'oppose': 's_oppose_à', 'diffère': 'diffère_de', 'differe': 'diffère_de',
    }

    def __init__(self, storage_path: str = 'data/concept_relations_default.json', use_spacy: bool = True):
        self.storage_path = storage_path
        self.relations: List[Dict[str, Any]] = []
        self._nlp = None
        if use_spacy:
            self._nlp = self._load_spacy()
        self.load()

    def _load_spacy(self):
        try:
            import spacy  # type: ignore
            for model in ('fr_core_news_md', 'fr_core_news_sm'):
                try:
                    return spacy.load(model)
                except Exception:
                    continue
        except Exception:
            return None
        return None

    def digest_text(self, text: str, *, source: str = 'book', limit: int = 220) -> Dict[str, Any]:
        sentences = self._sentences(text, limit=limit)
        extracted: List[Dict[str, Any]] = []
        for sent in sentences:
            rels = self._extract_with_spacy(sent) if self._nlp is not None else []
            if not rels:
                rels = self._extract_with_patterns(sent)
            extracted.extend(rels)

        accepted = []
        for rel in extracted:
            clean = self._clean_relation(rel, source=source)
            if clean:
                accepted.append(clean)
        merged = self._merge_relations(accepted)
        self._absorb(merged)
        self.save()
        return {
            'available': True,
            'source': source,
            'relations_extracted': len(merged),
            'relations': merged[:80],
            'spacy_used': self._nlp is not None,
            'concepts': self.top_concepts(24),
            'created_at': time.time(),
        }

    def query(self, query_text: str, *, limit: int = 12) -> Dict[str, Any]:
        q_terms = self._query_terms(query_text)
        scored: List[Tuple[float, Dict[str, Any]]] = []
        for rel in self.relations:
            src = str(rel.get('source', ''))
            tgt = str(rel.get('target', ''))
            rtype = str(rel.get('relation', ''))
            bag = set(self._query_terms(' '.join([src, tgt, rtype])))
            overlap = len(set(q_terms) & bag)
            if not overlap:
                # concept proche par sous-chaîne normalisée
                qn = _strip_accents(' '.join(q_terms))
                rn = _strip_accents(' '.join(bag))
                if not any(t and t in rn for t in q_terms if len(t) >= 5):
                    continue
                overlap = 1
            confidence = float(rel.get('confidence', 0.45) or 0.45)
            recency = min(0.15, max(0.0, (float(rel.get('reinforced', 1) or 1) - 1) * 0.025))
            score = overlap * 0.55 + confidence * 0.35 + recency
            scored.append((score, rel))
        scored.sort(key=lambda x: x[0], reverse=True)
        selected = [dict(r, score=round(s, 4)) for s, r in scored[:limit]]
        atoms = []
        for r in selected:
            atoms.extend([r.get('source'), r.get('target'), r.get('relation')])
        return {
            'available': bool(selected),
            'query_terms': q_terms,
            'relations': selected,
            'active_concepts': self._unique_public(atoms, 18),
            'concept_pressures': self._pressures(selected),
        }

    def chain_query(
        self,
        query_text: str,
        *,
        depth: int = 2,
        limit: int = 16,
        decay: float = 0.72,
    ) -> Dict[str, Any]:
        """Traverse le graphe de relations par BFS jusqu'à `depth` niveaux.

        Exemple : query "temps" avec depth=2 peut activer :
          niveau 0 : durée –est→ temps          (match direct)
          niveau 1 : mémoire –est→ durée        (durée est un voisin de temps)
          niveau 2 : souvenir –précède→ mémoire (mémoire est voisin de durée)

        Chaque niveau supplémentaire reçoit un score multiplié par `decay`
        pour refléter l'éloignement conceptuel.

        Retourne le même format que query() + :
          - chain_paths : les chemins parcourus (source→relation→target)
          - max_depth_reached : profondeur réelle atteinte
        """
        # ---- niveau 0 : matching direct -----------------------------------
        base = self.query(query_text, limit=limit)
        if not base.get('relations'):
            return {**base, 'chain_paths': [], 'max_depth_reached': 0}

        # Construire un index source/target → relations pour BFS rapide
        src_index: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        tgt_index: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for rel in self.relations:
            src = _public_concept(rel.get('source'))
            tgt = _public_concept(rel.get('target'))
            if src:
                src_index[src].append(rel)
            if tgt:
                tgt_index[tgt].append(rel)

        # Ensemble de concepts actifs à ce niveau
        active: set[str] = set()
        for rel in base['relations']:
            for key in ('source', 'target'):
                c = _public_concept(rel.get(key))
                if c:
                    active.add(c)

        visited: set[str] = set(active)
        chain_relations: List[Dict[str, Any]] = list(base['relations'])
        chain_paths: List[str] = []
        max_depth_reached = 0

        # ---- BFS sur les niveaux 1..depth --------------------------------
        for level in range(1, depth + 1):
            if not active:
                break
            next_active: set[str] = set()
            level_score_factor = decay ** level

            for concept in active:
                # Voisins : concept est source → regarder targets
                for rel in src_index.get(concept, []):
                    tgt = _public_concept(rel.get('target'))
                    if not tgt or tgt in visited:
                        continue
                    score = float(rel.get('confidence', 0.5) or 0.5) * level_score_factor
                    chain_relations.append(dict(
                        rel,
                        score=round(score, 4),
                        chain_depth=level,
                        chain_via=concept,
                    ))
                    path = (
                        f"{_public_concept(rel.get('source'))}"
                        f" –{rel.get('relation', '?')}→ {tgt}"
                        f" [via {concept}, d{level}]"
                    )
                    chain_paths.append(path)
                    visited.add(tgt)
                    next_active.add(tgt)

                # Voisins : concept est target → regarder sources
                for rel in tgt_index.get(concept, []):
                    src = _public_concept(rel.get('source'))
                    if not src or src in visited:
                        continue
                    score = float(rel.get('confidence', 0.5) or 0.5) * level_score_factor * 0.85
                    chain_relations.append(dict(
                        rel,
                        score=round(score, 4),
                        chain_depth=level,
                        chain_via=concept,
                    ))
                    path = (
                        f"{src} –{rel.get('relation', '?')}→"
                        f" {_public_concept(rel.get('target'))}"
                        f" [via {concept}, d{level}]"
                    )
                    chain_paths.append(path)
                    visited.add(src)
                    next_active.add(src)

            if next_active:
                max_depth_reached = level
            active = next_active

        # ---- Déduplication et tri par score --------------------------------
        seen_keys: set[tuple] = set()
        deduped: List[Dict[str, Any]] = []
        for r in chain_relations:
            key = (
                _public_concept(r.get('source')),
                r.get('relation', ''),
                _public_concept(r.get('target')),
            )
            if key not in seen_keys:
                seen_keys.add(key)
                deduped.append(r)

        deduped.sort(key=lambda r: float(r.get('score', 0.0) or 0.0), reverse=True)
        deduped = deduped[:limit]

        # Reconstruire active_concepts et concept_pressures
        atoms: List[Any] = []
        for r in deduped:
            atoms.extend([r.get('source'), r.get('target'), r.get('relation')])

        return {
            'available': bool(deduped),
            'query_terms': base.get('query_terms', []),
            'relations': deduped,
            'active_concepts': self._unique_public(atoms, 24),
            'concept_pressures': self._pressures(deduped),
            'chain_paths': chain_paths[:12],
            'max_depth_reached': max_depth_reached,
        }

    def snapshot(self) -> Dict[str, Any]:
        return {
            'available': True,
            'relations': len(self.relations),
            'top_concepts': self.top_concepts(12),
            'spacy_ready': self._nlp is not None,
        }

    def top_concepts(self, limit: int = 20) -> List[str]:
        c = Counter()
        for r in self.relations:
            for key in ('source', 'target'):
                val = _public_concept(r.get(key))
                if val:
                    c[val] += int(r.get('reinforced', 1) or 1)
        return [k for k, _ in c.most_common(limit)]

    def _sentences(self, text: str, limit: int = 220) -> List[str]:
        raw = re.split(r'(?<=[.!?…])\s+', str(text or ''))
        out = []
        for s in raw:
            s = re.sub(r'\s+', ' ', s).strip()
            if 18 <= len(s) <= 420:
                out.append(s)
            if len(out) >= limit:
                break
        return out

    def _extract_with_spacy(self, sentence: str) -> List[Dict[str, Any]]:
        if self._nlp is None:
            return []
        try:
            doc = self._nlp(sentence)
        except Exception:
            return []
        rels: List[Dict[str, Any]] = []
        for tok in doc:
            lemma = _norm(getattr(tok, 'lemma_', '') or tok.text)
            reltype = self.RELATION_ALIASES.get(lemma)
            if not reltype:
                continue
            neg = any(child.dep_ in ('neg', 'advmod') and _norm(child.text) in {'ne','pas','jamais','plus','aucun'} for child in tok.children)
            if neg and reltype == 'est':
                reltype = "n'est_pas"
            subj = None
            obj = None
            for child in tok.children:
                if child.dep_ in ('nsubj', 'nsubj:pass', 'csubj'):
                    subj = self._span_text(child)
                if child.dep_ in ('obj', 'obl', 'attr', 'xcomp', 'acomp'):
                    obj = self._span_text(child)
            if subj and obj:
                rels.append({'source': subj, 'relation': reltype, 'target': obj, 'evidence': sentence, 'confidence': 0.74})
        return rels

    def _span_text(self, token: Any) -> str:
        try:
            subtree = list(token.subtree)
            subtree.sort(key=lambda t: t.i)
            return ' '.join(t.text for t in subtree)
        except Exception:
            return str(getattr(token, 'text', token))

    def _extract_with_patterns(self, sentence: str) -> List[Dict[str, Any]]:
        s = re.sub(r'\s+', ' ', sentence).strip()
        patterns = [
            (r"(?P<src>[A-Za-zÀ-ÿ'\- ]{3,60})\s+n['’]?est\s+pas\s+(?:un|une|du|de la|des|le|la|les)?\s*(?P<tgt>[A-Za-zÀ-ÿ'\- ]{3,80})", "n'est_pas", 0.70),
            (r"(?P<src>[A-Za-zÀ-ÿ'\- ]{3,60})\s+ne\s+(?:se\s+)?réduit\s+pas\s+à\s+(?P<tgt>[A-Za-zÀ-ÿ'\- ]{3,80})", "n'est_pas", 0.72),
            (r"(?P<src>[A-Za-zÀ-ÿ'\- ]{3,60})\s+(?:est|sont)\s+(?:un|une|du|de la|des|le|la|les)?\s*(?P<tgt>[A-Za-zÀ-ÿ'\- ]{3,80})", 'est', 0.62),
            (r"(?P<src>[A-Za-zÀ-ÿ'\- ]{3,60})\s+(?:contient|comprend|porte|garde)\s+(?P<tgt>[A-Za-zÀ-ÿ'\- ]{3,80})", 'contient', 0.60),
            (r"(?P<src>[A-Za-zÀ-ÿ'\- ]{3,60})\s+(?:précède|precede|vient\s+avant)\s+(?P<tgt>[A-Za-zÀ-ÿ'\- ]{3,80})", 'précède', 0.66),
            (r"(?P<src>[A-Za-zÀ-ÿ'\- ]{3,60})\s+(?:reçoit|recoit|perçoit|percoit)\s+(?P<tgt>[A-Za-zÀ-ÿ'\- ]{3,80})", 'reçoit', 0.58),
            (r"(?P<src>[A-Za-zÀ-ÿ'\- ]{3,60})\s+(?:dépend|depend)\s+de\s+(?P<tgt>[A-Za-zÀ-ÿ'\- ]{3,80})", 'dépend_de', 0.58),
        ]
        rels = []
        for pat, typ, conf in patterns:
            for m in re.finditer(pat, s, flags=re.I):
                rels.append({'source': m.group('src'), 'relation': typ, 'target': m.group('tgt'), 'evidence': sentence, 'confidence': conf})
        return rels

    def _clean_relation(self, rel: Mapping[str, Any], *, source: str) -> Optional[Dict[str, Any]]:
        src = _public_concept(rel.get('source'))
        raw_tgt = str(rel.get('target') or '')
        raw_tgt = re.split(r'\s+(?:et|mais|donc|qui|que|car|puis)\s+(?:reçoit|recoit|est|sont|devient|contient|précède|precede|porte|garde)\b', raw_tgt, maxsplit=1, flags=re.I)[0]
        tgt = _public_concept(raw_tgt)
        rtype = _norm(rel.get('relation')) or 'lié'
        if rtype in {'n est pas', "n'est pas", 'nest pas', 'n pas'}:
            rtype = "n'est_pas"
        elif rtype in {'depend de', 'dépend de'}:
            rtype = 'dépend_de'
        if not src or not tgt or src == tgt:
            return None
        if len(src.split()) > 6 or len(tgt.split()) > 7:
            return None
        if any(x in {'question','réponse','reponse','utilisateur','leia'} for x in (src, tgt)):
            return None
        if rtype == 'est' and tgt in {'pas', 'ne pas'}:
            return None
        return {
            'source': src,
            'relation': rtype[:32],
            'target': tgt,
            'evidence': str(rel.get('evidence', ''))[:240],
            'confidence': round(float(rel.get('confidence', 0.5) or 0.5), 4),
            'source_doc': str(source or 'book')[:180],
            'created_at': time.time(),
            'reinforced': 1,
        }

    def _merge_relations(self, relations: Iterable[Mapping[str, Any]]) -> List[Dict[str, Any]]:
        merged: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
        for r in relations:
            key = (str(r.get('source')), str(r.get('relation')), str(r.get('target')))
            if key not in merged:
                merged[key] = dict(r)
            else:
                merged[key]['confidence'] = round(max(float(merged[key].get('confidence', 0)), float(r.get('confidence', 0))), 4)
                merged[key]['reinforced'] = int(merged[key].get('reinforced', 1)) + 1
        return list(merged.values())

    def _absorb(self, new_relations: Iterable[Mapping[str, Any]]) -> None:
        index = {(r.get('source'), r.get('relation'), r.get('target')): r for r in self.relations}
        for nr in new_relations:
            key = (nr.get('source'), nr.get('relation'), nr.get('target'))
            if key in index:
                old = index[key]
                old['confidence'] = round(max(float(old.get('confidence', 0)), float(nr.get('confidence', 0))), 4)
                old['reinforced'] = int(old.get('reinforced', 1) or 1) + int(nr.get('reinforced', 1) or 1)
                old['last_seen_at'] = time.time()
                if nr.get('evidence') and not old.get('evidence'):
                    old['evidence'] = nr.get('evidence')
            else:
                self.relations.append(dict(nr))
        self.relations = sorted(self.relations, key=lambda r: (float(r.get('confidence', 0)), int(r.get('reinforced', 1) or 1)), reverse=True)[:1200]

    def _query_terms(self, text: str) -> List[str]:
        s = _norm(text)
        words = [_public_concept(w) for w in s.split()]
        stop = {'est','quoi','pourquoi','comment','rapport','entre','avec','dans','pour','dire','dis','tu','me','cest','c','quoi'}
        return [w for w in words if w and w not in stop and len(w) >= 3][:16]

    def _pressures(self, relations: List[Mapping[str, Any]]) -> Dict[str, float]:
        p: Dict[str, float] = defaultdict(float)
        for i, r in enumerate(relations):
            base = max(0.25, 0.86 - i * 0.055) * float(r.get('confidence', 0.55) or 0.55)
            for key in ('source', 'target'):
                c = _public_concept(r.get(key))
                if c:
                    p[c] = max(p[c], min(1.0, base))
        return dict(p)

    def _unique_public(self, values: Iterable[Any], limit: int) -> List[str]:
        out = []
        seen = set()
        for v in values:
            c = _public_concept(v)
            if c and c not in seen:
                seen.add(c); out.append(c)
            if len(out) >= limit:
                break
        return out

    def save(self) -> None:
        os.makedirs(os.path.dirname(self.storage_path) or '.', exist_ok=True)
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump({'relations': self.relations}, f, ensure_ascii=False, indent=2)

    def load(self) -> None:
        if not os.path.exists(self.storage_path):
            return
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if isinstance(data.get('relations'), list):
                self.relations = [r for r in data['relations'] if isinstance(r, Mapping)]
        except Exception:
            self.relations = []
