# emotional_knowledge_digestion.py
# Project Leia / project_leia
#
# Objectif:
#   Transformer un livre, un PDF ou un texte en matière mentale vivante:
#   passage -> compréhension locale -> réaction cognitive -> concepts -> liens mémoire
#   -> traces émotionnelles -> réactivation future -> influence du dialogue.
#
# Important:
#   - zéro réponse préécrite
#   - zéro "si question X alors phrase Y"
#   - pas de chatbot RAG classique
#   - pas de simple knowledge cutoff
#   - le texte est digéré progressivement, avec importance, confusion,
#     résonance, curiosité, stabilité, liens, oubli et réactivation.
#
# Dépendances:
#   Standard library uniquement.
#   Optionnel: si tu veux lire les PDF directement, installe pypdf:
#       pip install pypdf
#
# Utilisation simple:
#   from emotional_knowledge_digestion import EmotionalKnowledgeDigestion
#
#   digestion = EmotionalKnowledgeDigestion(memory_system=memory)
#   result = digestion.digest_text("texte du livre", source="livre_x")
#   digestion.integrate_with_memory()
#
# Utilisation PDF:
#   result = digestion.digest_pdf("mon_livre.pdf", source="mon_livre")
#
# Branchement conseillé dans Leia:
#   1. Quand un livre est ajouté:
#        digestion.digest_pdf(path)
#   2. Après digestion:
#        digestion.integrate_with_memory()
#   3. Avant réponse dialogue:
#        active = digestion.reactivate_for_context(user_text)
#        payload["digested_memory"] = active
#   4. Le language generator utilise active["concept_pressures"],
#      active["semantic_atoms"], active["emotional_bias"].


from __future__ import annotations

import json
import math
import os
import re
import time
import uuid
from collections import Counter, defaultdict, deque
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Deque, Dict, Iterable, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Outils généraux
# ---------------------------------------------------------------------------

_WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9_'-]+", re.UNICODE)
_SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?…])\s+|\n{2,}", re.UNICODE)

FRENCH_STOPWORDS = {
    "a", "à", "afin", "ai", "aie", "aient", "aies", "ait", "alors", "as", "au",
    "aucun", "aussi", "autre", "aux", "avaient", "avais", "avait", "avant",
    "avec", "avez", "avoir", "avons", "ayant", "b", "bah", "beaucoup", "bien",
    "bon", "c", "ça", "car", "ce", "ceci", "cela", "celle", "celles", "celui",
    "ces", "cet", "cette", "ceux", "chaque", "chez", "ci", "comme", "comment",
    "d", "dans", "de", "des", "deux", "devant", "doit", "donc", "dont", "du",
    "elle", "elles", "en", "encore", "entre", "es", "est", "et", "étaient",
    "étais", "était", "étant", "été", "être", "eu", "eux", "f", "fait", "fois",
    "font", "g", "h", "i", "ici", "il", "ils", "j", "je", "jusqu", "k", "l",
    "la", "là", "le", "les", "leur", "leurs", "lui", "m", "ma", "mais", "me",
    "même", "mes", "moi", "mon", "n", "ne", "ni", "nos", "notre", "nous",
    "o", "on", "ont", "ou", "où", "p", "par", "parce", "pas", "pendant",
    "peu", "peut", "plus", "pour", "pourquoi", "q", "qu", "quand", "que",
    "quel", "quelle", "qui", "r", "s", "sa", "sans", "se", "ses", "si",
    "son", "sont", "sous", "sur", "t", "ta", "te", "tes", "toi", "ton", "tous",
    "tout", "toute", "toutes", "tu", "u", "un", "une", "v", "va", "vais", "vers",
    "vos", "votre", "vous", "w", "x", "y", "z",
}


def now_ts() -> float:
    return time.time()


def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, float(x)))



def _safe_mean(values: Iterable[Any]) -> float:
    nums = []
    for value in values:
        try:
            f = float(value)
        except Exception:
            continue
        if not math.isnan(f) and not math.isinf(f):
            nums.append(f)
    if not nums:
        return 0.0
    return sum(nums) / len(nums)

def normalize_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def tokenize(text: str) -> List[str]:
    return [w.lower().strip("'_-") for w in _WORD_RE.findall(text) if w.strip("'_-")]


def content_words(text: str) -> List[str]:
    words = tokenize(text)
    return [
        w for w in words
        if len(w) > 2
        and w not in FRENCH_STOPWORDS
        and not w.isdigit()
    ]


def split_sentences(text: str) -> List[str]:
    parts = [p.strip() for p in _SENTENCE_SPLIT_RE.split(text) if p.strip()]
    out: List[str] = []
    for p in parts:
        if len(p) > 900:
            chunks = chunk_text(p, max_chars=700, overlap_chars=80)
            out.extend(chunks)
        else:
            out.append(p)
    return out


def chunk_text(text: str, max_chars: int = 1800, overlap_chars: int = 180) -> List[str]:
    text = normalize_text(text)
    if not text:
        return []

    sentences = split_sentences(text) if len(text) > max_chars else [text]
    chunks: List[str] = []
    current = ""

    for s in sentences:
        if not current:
            current = s
            continue

        if len(current) + 1 + len(s) <= max_chars:
            current += " " + s
        else:
            chunks.append(current.strip())
            tail = current[-overlap_chars:] if overlap_chars > 0 else ""
            current = (tail + " " + s).strip()

    if current:
        chunks.append(current.strip())

    return chunks


def cosine_from_counters(a: Counter, b: Counter) -> float:
    if not a or not b:
        return 0.0
    keys = set(a) | set(b)
    dot = sum(a.get(k, 0.0) * b.get(k, 0.0) for k in keys)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    if na <= 1e-9 or nb <= 1e-9:
        return 0.0
    return clamp(dot / (na * nb))


def keyword_counter(text: str) -> Counter:
    return Counter(content_words(text))


def safe_json_load(path: Path, default: Any) -> Any:
    try:
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        pass
    return default


def safe_json_save(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


# ---------------------------------------------------------------------------
# Structures vivantes
# ---------------------------------------------------------------------------

@dataclass
class SemanticAtom:
    """Petite unité de sens extraite d'un passage.

    Ce n'est pas une phrase préécrite pour parler.
    C'est une matière conceptuelle que Leia peut relier à sa mémoire.
    """

    atom_id: str
    surface: str
    keywords: List[str]
    source: str
    passage_id: str
    created_at: float
    importance: float
    novelty: float
    clarity: float
    density: float


@dataclass
class EmotionalReaction:
    """Réaction cognitive/affective à une idée lue.

    Les valeurs ne dictent pas de phrase.
    Elles modulent les liens, l'activation et l'expression future.
    """

    resonance: float = 0.0
    curiosity: float = 0.0
    friction: float = 0.0
    familiarity: float = 0.0
    uncertainty: float = 0.0
    attraction: float = 0.0
    resistance: float = 0.0
    calm: float = 0.0


@dataclass
class DigestedNeuron:
    """Neurone conceptuel créé depuis lecture ou renforcé par lecture."""

    neuron_id: str
    label: str
    keywords: List[str]
    source_refs: List[str] = field(default_factory=list)
    activation: float = 0.0
    stability: float = 0.0
    emotional_weight: float = 0.0
    curiosity: float = 0.0
    uncertainty: float = 0.0
    created_at: float = field(default_factory=now_ts)
    updated_at: float = field(default_factory=now_ts)
    use_count: int = 0


@dataclass
class MemoryLink:
    """Lien entre deux neurones ou entre un neurone et une trace."""

    link_id: str
    source_id: str
    target_id: str
    relation: str
    weight: float
    emotional_tone: float
    evidence_count: int = 1
    created_at: float = field(default_factory=now_ts)
    updated_at: float = field(default_factory=now_ts)


@dataclass
class DigestionTrace:
    """Trace vécue d'un passage digéré."""

    trace_id: str
    source: str
    passage_id: str
    timestamp: float
    atoms: List[SemanticAtom]
    reaction: EmotionalReaction
    created_neurons: List[str]
    reinforced_neurons: List[str]
    unresolved_questions: List[str]
    stability_delta: float
    raw_excerpt: str = ""


@dataclass
class DigestionResult:
    source: str
    started_at: float
    finished_at: float
    passages_read: int
    atoms_created: int
    neurons_created: int
    neurons_reinforced: int
    links_created: int
    unresolved_count: int
    traces: List[DigestionTrace]


# ---------------------------------------------------------------------------
# Digestion émotionnelle
# ---------------------------------------------------------------------------

class EmotionalKnowledgeDigestion:
    """Moteur de digestion émotionnelle de connaissances pour Leia.

    Le moteur peut fonctionner seul, mais il accepte aussi un memory_system externe.
    Il ne suppose pas une API unique: il essaie plusieurs méthodes courantes
    avec prudence pour rester branchable sur tes fichiers existants.
    """

    def __init__(
        self,
        memory_system: Optional[Any] = None,
        storage_dir: str | os.PathLike[str] = "data/digestion_memory",
        max_recent_traces: int = 80,
    ) -> None:
        self.memory_system = memory_system
        self.storage_dir = Path(storage_dir)
        self.neurons_path = self.storage_dir / "digested_neurons.json"
        self.links_path = self.storage_dir / "digested_links.json"
        self.traces_path = self.storage_dir / "digestion_traces.json"

        self.neurons: Dict[str, DigestedNeuron] = {}
        self.links: Dict[str, MemoryLink] = {}
        self.traces: Deque[DigestionTrace] = deque(maxlen=max_recent_traces)

        # Etat vivant optionnel de Leia.
        # Il permet à la lecture d'être digérée selon son état actuel
        # sans transformer le module en système de réponses préécrites.
        self.current_leia_state: Dict[str, Any] = {}

        self._load_state()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _load_state(self) -> None:
        raw_neurons = safe_json_load(self.neurons_path, {})
        raw_links = safe_json_load(self.links_path, {})
        raw_traces = safe_json_load(self.traces_path, [])

        for nid, payload in raw_neurons.items():
            try:
                self.neurons[nid] = DigestedNeuron(**payload)
            except Exception:
                continue

        for lid, payload in raw_links.items():
            try:
                self.links[lid] = MemoryLink(**payload)
            except Exception:
                continue

        for payload in raw_traces[-self.traces.maxlen:]:
            try:
                atoms = [SemanticAtom(**a) for a in payload.get("atoms", [])]
                reaction = EmotionalReaction(**payload.get("reaction", {}))
                payload = dict(payload)
                payload["atoms"] = atoms
                payload["reaction"] = reaction
                self.traces.append(DigestionTrace(**payload))
            except Exception:
                continue

    def save_state(self) -> None:
        """Persist all digested knowledge layers.

        Important: older builds only saved neurons. That made PDF reading look
        successful while links and recent traces disappeared after the run, so
        Leia had concepts but no lived/retrievable reading trace.
        """
        safe_json_save(self.neurons_path, {k: asdict(v) for k, v in self.neurons.items()})
        safe_json_save(self.links_path, {k: asdict(v) for k, v in self.links.items()})
        safe_json_save(self.traces_path, [asdict(t) for t in self.traces])
        safe_json_save(self.links_path, {k: asdict(v) for k, v in self.links.items()})
        safe_json_save(self.traces_path, [asdict(t) for t in self.traces])

    # ------------------------------------------------------------------
    # Lecture de fichiers
    # ------------------------------------------------------------------

    def read_pdf_text(self, pdf_path: str | os.PathLike[str]) -> str:
        """Lit un PDF si pypdf est installé.

        Si pypdf n'est pas installé, l'erreur explique quoi faire.
        """
        try:
            from pypdf import PdfReader  # type: ignore
        except Exception as exc:
            raise RuntimeError(
                "Lecture PDF impossible: installe pypdf avec `pip install pypdf`, "
                "ou donne déjà le texte extrait à digest_text()."
            ) from exc

        reader = PdfReader(str(pdf_path))
        pages: List[str] = []
        for page in reader.pages:
            try:
                pages.append(page.extract_text() or "")
            except Exception:
                pages.append("")
        return normalize_text("\n\n".join(pages))

    def digest_pdf(
        self,
        pdf_path: str | os.PathLike[str],
        source: Optional[str] = None,
        max_chars_per_passage: int = 1800,
    ) -> DigestionResult:
        path = Path(pdf_path)
        text = self.read_pdf_text(path)
        return self.digest_text(
            text,
            source=source or path.stem,
            max_chars_per_passage=max_chars_per_passage,
        )

    # ------------------------------------------------------------------
    # Pipeline principal
    # ------------------------------------------------------------------

    def digest_text(
        self,
        text: str,
        source: str = "unknown_source",
        max_chars_per_passage: int = 1800,
        save: bool = True,
    ) -> DigestionResult:
        started = now_ts()
        text = normalize_text(text)
        passages = chunk_text(text, max_chars=max_chars_per_passage)

        all_traces: List[DigestionTrace] = []
        before_neurons = len(self.neurons)
        before_links = len(self.links)
        reinforced_total = 0

        for idx, passage in enumerate(passages):
            trace = self.digest_passage(
                passage=passage,
                source=source,
                passage_index=idx,
                total_passages=len(passages),
            )
            reinforced_total += len(trace.reinforced_neurons)
            all_traces.append(trace)
            self.traces.append(trace)

        if save:
            self.save_state()

        return DigestionResult(
            source=source,
            started_at=started,
            finished_at=now_ts(),
            passages_read=len(passages),
            atoms_created=sum(len(t.atoms) for t in all_traces),
            neurons_created=max(0, len(self.neurons) - before_neurons),
            neurons_reinforced=reinforced_total,
            links_created=max(0, len(self.links) - before_links),
            unresolved_count=sum(len(t.unresolved_questions) for t in all_traces),
            traces=all_traces,
        )

    def digest_passage(
        self,
        passage: str,
        source: str,
        passage_index: int = 0,
        total_passages: int = 1,
    ) -> DigestionTrace:
        passage = normalize_text(passage)
        passage_id = self._new_id("passage")
        atoms = self.extract_semantic_atoms(passage, source, passage_id)
        reaction = self.measure_emotional_reaction(
            atoms,
            passage,
            leia_state=self.current_leia_state,
        )

        created: List[str] = []
        reinforced: List[str] = []

        for atom in atoms:
            neuron, was_created = self.create_or_reinforce_neuron(atom, reaction)
            if was_created:
                created.append(neuron.neuron_id)
            else:
                reinforced.append(neuron.neuron_id)

        self.link_new_atoms_to_memory(atoms, reaction)
        unresolved = self.generate_unresolved_questions(atoms, reaction)

        trace = DigestionTrace(
            trace_id=self._new_id("trace"),
            source=source,
            passage_id=passage_id,
            timestamp=now_ts(),
            atoms=atoms,
            reaction=reaction,
            created_neurons=created,
            reinforced_neurons=reinforced,
            unresolved_questions=unresolved,
            stability_delta=self._compute_stability_delta(reaction, atoms),
            raw_excerpt=passage[:700],
        )

        self._soft_decay()
        return trace

    # ------------------------------------------------------------------
    # Extraction du sens
    # ------------------------------------------------------------------

    def extract_semantic_atoms(
        self,
        passage: str,
        source: str,
        passage_id: str,
        max_atoms: int = 8,
    ) -> List[SemanticAtom]:
        sentences = split_sentences(passage)
        global_counts = keyword_counter(passage)

        candidates: List[Tuple[float, str, List[str]]] = []

        for sentence in sentences:
            words = content_words(sentence)
            if len(words) < 2:
                continue

            counts = Counter(words)
            density = len(set(words)) / max(1, len(tokenize(sentence)))
            rarity_signal = sum(1.0 / (1.0 + global_counts[w]) for w in set(words))
            length_balance = 1.0 - min(1.0, abs(len(words) - 12) / 24.0)
            punctuation_signal = 0.08 if any(x in sentence for x in ["?", ":", ";"]) else 0.0

            score = (
                0.40 * density
                + 0.25 * length_balance
                + 0.25 * min(1.0, rarity_signal / max(1, len(set(words))))
                + punctuation_signal
            )

            top_keywords = [w for w, _ in counts.most_common(8)]
            candidates.append((score, sentence.strip(), top_keywords))

        candidates.sort(key=lambda x: x[0], reverse=True)
        selected = candidates[:max_atoms]

        atoms: List[SemanticAtom] = []
        for score, surface, keywords in selected:
            novelty = self._estimate_novelty(keywords)
            clarity = self._estimate_clarity(surface, keywords)
            density = len(set(keywords)) / max(1, len(tokenize(surface)))
            importance = clamp((score * 0.45) + (novelty * 0.25) + (clarity * 0.20) + (density * 0.10))

            atoms.append(
                SemanticAtom(
                    atom_id=self._new_id("atom"),
                    surface=surface,
                    keywords=keywords,
                    source=source,
                    passage_id=passage_id,
                    created_at=now_ts(),
                    importance=importance,
                    novelty=novelty,
                    clarity=clarity,
                    density=clamp(density),
                )
            )

        if not atoms and passage:
            words = content_words(passage)
            keywords = [w for w, _ in Counter(words).most_common(8)]
            atoms.append(
                SemanticAtom(
                    atom_id=self._new_id("atom"),
                    surface=passage[:500],
                    keywords=keywords,
                    source=source,
                    passage_id=passage_id,
                    created_at=now_ts(),
                    importance=0.35,
                    novelty=self._estimate_novelty(keywords),
                    clarity=self._estimate_clarity(passage, keywords),
                    density=0.25,
                )
            )

        return atoms

    def measure_emotional_reaction(
        self,
        atoms: List[SemanticAtom],
        passage: str,
        leia_state: Optional[Dict[str, Any]] = None,
    ) -> EmotionalReaction:
        """Mesure la réaction cognitive/affective à un passage.

        V2:
        - garde l'analyse locale originale;
        - ajoute l'influence de l'état actuel de Leia;
        - ajoute une texture rythmique/corporelle indirecte;
        - ne produit aucune phrase publique préécrite.
        """
        if not atoms:
            return EmotionalReaction(uncertainty=0.45, friction=0.22)

        novelty = sum(a.novelty for a in atoms) / len(atoms)
        clarity = sum(a.clarity for a in atoms) / len(atoms)
        importance = sum(a.importance for a in atoms) / len(atoms)
        density = sum(a.density for a in atoms) / len(atoms)

        familiarity = 1.0 - novelty
        uncertainty = clamp((1.0 - clarity) * 0.75 + density * 0.20)
        friction = clamp(uncertainty * 0.55 + novelty * 0.30)
        curiosity = clamp(novelty * 0.45 + importance * 0.35 + friction * 0.20)
        resonance = clamp(familiarity * 0.35 + importance * 0.45 + clarity * 0.20)
        attraction = clamp(curiosity * 0.55 + resonance * 0.35 + novelty * 0.10)
        resistance = clamp(friction * 0.75 + uncertainty * 0.25)
        calm = clamp(clarity * 0.55 + familiarity * 0.25 + (1.0 - friction) * 0.20)

        state = dict(self.current_leia_state or {})
        if leia_state:
            state.update(leia_state)

        if state:
            warmth = float(state.get("warmth", state.get("core_warmth", 0.50)) or 0.0)
            tension = float(state.get("tension", state.get("pressure", 0.25)) or 0.0)
            state_curiosity = float(state.get("curiosity", state.get("explore", 0.45)) or 0.0)
            fatigue = float(state.get("fatigue", 0.0) or 0.0)
            safety = float(state.get("emotional_safety", state.get("safety", 0.75)) or 0.0)
            openness = float(state.get("openness", state.get("availability", 0.55)) or 0.0)

            resonance = clamp(resonance + (warmth - 0.5) * 0.18 + openness * 0.08)
            friction = clamp(friction + tension * 0.18 + fatigue * 0.10 - safety * 0.06)
            curiosity = clamp(curiosity + state_curiosity * 0.22 + novelty * openness * 0.10)
            uncertainty = clamp(uncertainty + fatigue * 0.10 + tension * 0.07)
            calm = clamp(calm + safety * 0.10 + warmth * 0.07 - tension * 0.10)
            attraction = clamp(attraction + curiosity * 0.08 + warmth * 0.05)
            resistance = clamp(resistance + friction * 0.08 + fatigue * 0.06)

        return EmotionalReaction(
            resonance=resonance,
            curiosity=curiosity,
            friction=friction,
            familiarity=familiarity,
            uncertainty=uncertainty,
            attraction=attraction,
            resistance=resistance,
            calm=calm,
        )

    # ------------------------------------------------------------------
    # Neurones et liens
    # ------------------------------------------------------------------

    def create_or_reinforce_neuron(
        self,
        atom: SemanticAtom,
        reaction: EmotionalReaction,
    ) -> Tuple[DigestedNeuron, bool]:
        existing = self._find_best_existing_neuron(atom.keywords)
        emotional_weight = clamp(
            reaction.resonance * 0.35
            + reaction.curiosity * 0.35
            + reaction.friction * 0.20
            + atom.importance * 0.10
        )

        if existing is None:
            label = self._make_label(atom)
            neuron = DigestedNeuron(
                neuron_id=self._new_id("neuron"),
                label=label,
                keywords=list(dict.fromkeys(atom.keywords[:10])),
                source_refs=[f"{atom.source}:{atom.passage_id}:{atom.atom_id}"],
                activation=clamp(0.25 + atom.importance * 0.45 + reaction.curiosity * 0.20),
                stability=clamp(0.10 + atom.clarity * 0.25 + reaction.resonance * 0.25),
                emotional_weight=emotional_weight,
                curiosity=reaction.curiosity,
                uncertainty=reaction.uncertainty,
            )
            self.neurons[neuron.neuron_id] = neuron
            self._push_to_external_memory(neuron, atom, reaction)
            return neuron, True

        neuron = existing
        neuron.updated_at = now_ts()
        neuron.use_count += 1
        neuron.source_refs.append(f"{atom.source}:{atom.passage_id}:{atom.atom_id}")
        neuron.source_refs = neuron.source_refs[-20:]

        for kw in atom.keywords:
            if kw not in neuron.keywords:
                neuron.keywords.append(kw)
        neuron.keywords = neuron.keywords[:16]

        neuron.activation = clamp(neuron.activation * 0.70 + (0.30 + atom.importance * 0.60) * 0.30)
        neuron.stability = clamp(neuron.stability + 0.04 * atom.clarity + 0.03 * reaction.resonance)
        neuron.emotional_weight = clamp(neuron.emotional_weight * 0.72 + emotional_weight * 0.28)
        neuron.curiosity = clamp(neuron.curiosity * 0.65 + reaction.curiosity * 0.35)
        neuron.uncertainty = clamp(neuron.uncertainty * 0.70 + reaction.uncertainty * 0.30)

        self._push_to_external_memory(neuron, atom, reaction)
        return neuron, False

    def link_new_atoms_to_memory(
        self,
        atoms: List[SemanticAtom],
        reaction: EmotionalReaction,
        max_links_per_atom: int = 5,
    ) -> None:
        if not atoms:
            return

        for atom in atoms:
            source_neuron = self._find_best_existing_neuron(atom.keywords)
            if source_neuron is None:
                continue

            candidates: List[Tuple[float, DigestedNeuron]] = []
            atom_counter = Counter(atom.keywords)

            for neuron in self.neurons.values():
                if neuron.neuron_id == source_neuron.neuron_id:
                    continue
                score = cosine_from_counters(atom_counter, Counter(neuron.keywords))
                score += 0.10 * neuron.activation
                score += 0.08 * neuron.emotional_weight
                if score > 0.18:
                    candidates.append((score, neuron))

            candidates.sort(key=lambda x: x[0], reverse=True)

            for score, target in candidates[:max_links_per_atom]:
                relation = self._infer_relation(atom, target, reaction)
                self._create_or_reinforce_link(
                    source_id=source_neuron.neuron_id,
                    target_id=target.neuron_id,
                    relation=relation,
                    weight=clamp(score * 0.55 + reaction.resonance * 0.20 + reaction.curiosity * 0.15),
                    emotional_tone=clamp(reaction.resonance - reaction.friction, -1.0, 1.0),
                )

    def _create_or_reinforce_link(
        self,
        source_id: str,
        target_id: str,
        relation: str,
        weight: float,
        emotional_tone: float,
    ) -> MemoryLink:
        stable_key = f"{source_id}|{target_id}|{relation}"
        existing_id = None
        for lid, link in self.links.items():
            if f"{link.source_id}|{link.target_id}|{link.relation}" == stable_key:
                existing_id = lid
                break

        if existing_id:
            link = self.links[existing_id]
            link.weight = clamp(link.weight * 0.78 + weight * 0.22)
            link.emotional_tone = clamp(link.emotional_tone * 0.80 + emotional_tone * 0.20, -1.0, 1.0)
            link.evidence_count += 1
            link.updated_at = now_ts()
            return link

        link = MemoryLink(
            link_id=self._new_id("link"),
            source_id=source_id,
            target_id=target_id,
            relation=relation,
            weight=weight,
            emotional_tone=emotional_tone,
        )
        self.links[link.link_id] = link
        self._push_link_to_external_memory(link)
        return link

    # ------------------------------------------------------------------
    # Réactivation pour dialogue
    # ------------------------------------------------------------------

    def reactivate_for_context(
        self,
        context_text: str,
        limit: int = 8,
    ) -> Dict[str, Any]:
        """Réactive les traces/concepts utiles pour une phrase utilisateur.

        Retour pensé pour être injecté dans le payload vivant de Leia.
        Aucun texte de réponse n'est imposé ici.
        """
        ctx_counter = keyword_counter(context_text)
        scored: List[Tuple[float, DigestedNeuron]] = []

        for neuron in self.neurons.values():
            semantic = cosine_from_counters(ctx_counter, Counter(neuron.keywords))
            warm_activation = neuron.activation * 0.25
            emotion = neuron.emotional_weight * 0.20
            curiosity = neuron.curiosity * 0.15
            uncertainty = neuron.uncertainty * 0.08
            score = semantic * 0.55 + warm_activation + emotion + curiosity + uncertainty
            if score > 0.06:
                scored.append((score, neuron))

        scored.sort(key=lambda x: x[0], reverse=True)
        active = scored[:limit]

        for score, neuron in active:
            neuron.activation = clamp(neuron.activation + 0.05 + score * 0.08)
            neuron.use_count += 1
            neuron.updated_at = now_ts()

        linked = self._collect_linked_neurons([n.neuron_id for _, n in active], limit=limit)

        concept_pressures: Dict[str, float] = {}
        semantic_atoms: List[Dict[str, Any]] = []

        for score, neuron in active:
            pressure = clamp(score * 0.65 + neuron.emotional_weight * 0.25 + neuron.curiosity * 0.10)
            concept_pressures[neuron.label] = pressure
            semantic_atoms.append({
                "label": neuron.label,
                "keywords": neuron.keywords[:8],
                "activation": neuron.activation,
                "stability": neuron.stability,
                "emotional_weight": neuron.emotional_weight,
                "curiosity": neuron.curiosity,
                "uncertainty": neuron.uncertainty,
                "pressure": pressure,
            })

        emotional_bias = self._build_emotional_bias([n for _, n in active])

        self.save_state()

        return {
            "active_concepts": [n.label for _, n in active],
            "linked_concepts": linked,
            "concept_pressures": concept_pressures,
            "semantic_atoms": semantic_atoms,
            "emotional_bias": emotional_bias,
            "unresolved_questions": self._recent_unresolved_questions(limit=5),
        }


    def build_conceptual_synthesis(
        self,
        context_text: str = "",
        *,
        limit: int = 10,
        source_hint: str = "",
    ) -> Dict[str, Any]:
        """Construit une synthèse conceptuelle interne depuis les traces lues.

        Ce n'est pas une réponse publique préécrite. La méthode compresse les
        neurones, mots-clés, liens et traces en axes utilisables par les moteurs
        de langage. Elle sert à passer de "j'ai des traces" à "je peux reformuler
        depuis des concepts".
        """
        ctx = keyword_counter(" ".join([str(context_text or ""), str(source_hint or "")]))
        ranked: List[Tuple[float, DigestedNeuron]] = []
        for neuron in self.neurons.values():
            kw = Counter(neuron.keywords or [])
            semantic = cosine_from_counters(ctx, kw) if ctx else 0.0
            structural = clamp(
                neuron.activation * 0.24
                + neuron.stability * 0.24
                + neuron.emotional_weight * 0.20
                + neuron.curiosity * 0.14
                + min(1.0, neuron.use_count / 12.0) * 0.10
                + len(neuron.source_refs) / 30.0
            )
            score = clamp(semantic * 0.52 + structural * 0.48)
            if score > 0.025:
                ranked.append((score, neuron))
        ranked.sort(key=lambda item: item[0], reverse=True)
        chosen = ranked[:max(1, int(limit or 10))]

        # Si la question ne matche pas bien, garder quand même les neurones les
        # plus stables pour éviter qu'un livre entier reste muet.
        if not chosen:
            chosen = sorted(
                [(clamp(n.stability * 0.45 + n.activation * 0.30 + n.emotional_weight * 0.25), n) for n in self.neurons.values()],
                key=lambda item: item[0],
                reverse=True,
            )[:max(1, int(limit or 10))]

        keyword_scores: Counter[str] = Counter()
        axes: List[Dict[str, Any]] = []
        chosen_ids = {n.neuron_id for _, n in chosen}
        for score, neuron in chosen:
            for kw in neuron.keywords[:12]:
                keyword_scores[str(kw)] += score + neuron.stability * 0.25 + neuron.emotional_weight * 0.18
            axes.append({
                "label": neuron.label,
                "keywords": list(dict.fromkeys(neuron.keywords[:8])),
                "pressure": round(clamp(score), 4),
                "stability": round(clamp(neuron.stability), 4),
                "curiosity": round(clamp(neuron.curiosity), 4),
                "uncertainty": round(clamp(neuron.uncertainty), 4),
                "source_refs": list(neuron.source_refs[:4]),
            })

        relations: List[Dict[str, Any]] = []
        for link in sorted(self.links.values(), key=lambda l: (l.weight, l.evidence_count), reverse=True):
            if link.source_id in chosen_ids or link.target_id in chosen_ids:
                src = self.neurons.get(link.source_id)
                dst = self.neurons.get(link.target_id)
                if not src or not dst:
                    continue
                relations.append({
                    "from": src.label,
                    "to": dst.label,
                    "relation": link.relation,
                    "weight": round(clamp(link.weight), 4),
                    "evidence": int(link.evidence_count),
                })
            if len(relations) >= limit:
                break

        recent_excerpts: List[Dict[str, Any]] = []
        for tr in list(self.traces)[-min(len(self.traces), 18):]:
            excerpt = str(getattr(tr, "raw_excerpt", "") or "").strip()
            if not excerpt:
                continue
            tr_keywords = Counter([kw for atom in (getattr(tr, "atoms", []) or []) for kw in getattr(atom, "keywords", [])])
            rel = cosine_from_counters(ctx, tr_keywords) if ctx else 0.0
            resonance = _safe_mean([
                getattr(getattr(tr, "reaction", None), "resonance", 0.0),
                getattr(getattr(tr, "reaction", None), "curiosity", 0.0),
            ])
            recent_excerpts.append({
                "excerpt": excerpt[:260],
                "relevance": round(clamp(rel + resonance * 0.25), 4),
                "source": str(getattr(tr, "source", "")),
                "keywords": list(tr_keywords.keys())[:8],
            })
        recent_excerpts.sort(key=lambda x: x.get("relevance", 0.0), reverse=True)

        top_keywords = [k for k, _ in keyword_scores.most_common(18) if len(k) > 2]
        density = clamp(len(self.neurons) / 80.0 + len(self.links) / 160.0)
        coherence = clamp(_safe_mean([a.get("stability", 0.0) for a in axes]) * 0.55 + len(relations) / max(1, limit) * 0.35 + density * 0.10)
        question_pressure = clamp(_safe_mean([a.get("uncertainty", 0.0) for a in axes]) * 0.55 + _safe_mean([a.get("curiosity", 0.0) for a in axes]) * 0.35)

        return {
            "available": bool(axes or top_keywords),
            "source": "conceptual_synthesis",
            "axes": axes,
            "relations": relations,
            "top_keywords": top_keywords,
            "recent_excerpts": recent_excerpts[:6],
            "unresolved_questions": self._recent_unresolved_questions(limit=6),
            "metrics": {
                "neurons_total": len(self.neurons),
                "links_total": len(self.links),
                "traces_total": len(self.traces),
                "density": round(density, 4),
                "coherence": round(coherence, 4),
                "question_pressure": round(question_pressure, 4),
            },
        }

    def integrate_with_payload(
        self,
        payload: Dict[str, Any],
        context_text: str,
        key: str = "digested_memory",
    ) -> Dict[str, Any]:
        """Helper direct pour leia_living_core.py."""
        payload = dict(payload or {})
        payload[key] = self.reactivate_for_context(context_text)
        return payload

    # ------------------------------------------------------------------
    # Questions non résolues
    # ------------------------------------------------------------------

    def generate_unresolved_questions(
        self,
        atoms: List[SemanticAtom],
        reaction: EmotionalReaction,
        max_questions: int = 3,
    ) -> List[str]:
        """Produit des axes de question, pas des phrases publiques fixes.

        Ces chaînes servent de matière interne.
        Elles ne doivent pas être sorties directement comme réponse finale.
        """
        if not atoms:
            return []

        questions: List[str] = []
        strongest = sorted(
            atoms,
            key=lambda a: a.novelty + reaction.uncertainty + reaction.curiosity,
            reverse=True,
        )[:max_questions]

        for atom in strongest:
            if reaction.uncertainty > 0.45:
                questions.append(self._axis_string("clarifier", atom.keywords))
            elif reaction.curiosity > 0.55:
                questions.append(self._axis_string("explorer", atom.keywords))
            elif reaction.friction > 0.45:
                questions.append(self._axis_string("résoudre_friction", atom.keywords))
            else:
                questions.append(self._axis_string("relier", atom.keywords))

        return questions[:max_questions]

    # ------------------------------------------------------------------
    # Maintenance vivante
    # ------------------------------------------------------------------

    def tick(self, elapsed_seconds: float = 1.0) -> None:
        """À appeler parfois dans la boucle vivante.

        Cela permet oubli léger + stabilisation progressive.
        """
        decay = clamp(elapsed_seconds / 3600.0, 0.0, 0.03)

        for neuron in self.neurons.values():
            neuron.activation = clamp(neuron.activation - decay * 0.45)
            if neuron.use_count > 1 and neuron.emotional_weight > 0.25:
                neuron.stability = clamp(neuron.stability + decay * 0.20)

        for link in self.links.values():
            link.weight = clamp(link.weight - decay * 0.20)

        self._prune_weak_links()
        self.save_state()

    def export_state(self) -> Dict[str, Any]:
        return {
            "neurons": {k: asdict(v) for k, v in self.neurons.items()},
            "links": {k: asdict(v) for k, v in self.links.items()},
            "traces": [asdict(t) for t in self.traces],
        }

    # ------------------------------------------------------------------
    # Internes: estimation
    # ------------------------------------------------------------------

    def _estimate_novelty(self, keywords: List[str]) -> float:
        if not keywords:
            return 0.5

        best = 0.0
        kc = Counter(keywords)
        for neuron in self.neurons.values():
            best = max(best, cosine_from_counters(kc, Counter(neuron.keywords)))
        return clamp(1.0 - best)

    def _estimate_clarity(self, surface: str, keywords: List[str]) -> float:
        tokens = tokenize(surface)
        if not tokens:
            return 0.0

        keyword_ratio = len(set(keywords)) / max(1, len(tokens))
        length_score = 1.0 - min(1.0, abs(len(tokens) - 22) / 60.0)
        punctuation_noise = min(0.30, surface.count("(") * 0.04 + surface.count("[") * 0.04)
        digit_noise = min(0.25, sum(t.isdigit() for t in tokens) / max(1, len(tokens)))

        return clamp(0.45 * length_score + 0.45 * keyword_ratio + 0.20 - punctuation_noise - digit_noise)

    def _find_best_existing_neuron(self, keywords: List[str]) -> Optional[DigestedNeuron]:
        if not keywords:
            return None

        kc = Counter(keywords)
        best_score = 0.0
        best_neuron: Optional[DigestedNeuron] = None

        for neuron in self.neurons.values():
            score = cosine_from_counters(kc, Counter(neuron.keywords))
            score += 0.04 * neuron.stability
            if score > best_score:
                best_score = score
                best_neuron = neuron

        if best_score >= 0.42:
            return best_neuron
        return None

    def _make_label(self, atom: SemanticAtom) -> str:
        kws = [k for k in atom.keywords if k not in FRENCH_STOPWORDS]
        if not kws:
            return "idée_" + atom.atom_id[-6:]
        return "_".join(kws[:3])[:80]

    def _infer_relation(
        self,
        atom: SemanticAtom,
        target: DigestedNeuron,
        reaction: EmotionalReaction,
    ) -> str:
        shared = set(atom.keywords) & set(target.keywords)

        if len(shared) >= 3:
            return "renforce"
        if reaction.friction > 0.55:
            return "met_en_tension"
        if reaction.curiosity > 0.58:
            return "ouvre_question"
        if reaction.resonance > 0.60:
            return "résonne_avec"
        return "associe"

    def _compute_stability_delta(
        self,
        reaction: EmotionalReaction,
        atoms: List[SemanticAtom],
    ) -> float:
        if not atoms:
            return 0.0
        clarity = sum(a.clarity for a in atoms) / len(atoms)
        importance = sum(a.importance for a in atoms) / len(atoms)
        return clamp(clarity * 0.35 + reaction.resonance * 0.35 + importance * 0.20 - reaction.friction * 0.10)

    def _build_emotional_bias(self, neurons: List[DigestedNeuron]) -> Dict[str, float]:
        if not neurons:
            return {
                "curiosity": 0.0,
                "uncertainty": 0.0,
                "resonance": 0.0,
                "semantic_pressure": 0.0,
            }

        curiosity = sum(n.curiosity for n in neurons) / len(neurons)
        uncertainty = sum(n.uncertainty for n in neurons) / len(neurons)
        resonance = sum(n.emotional_weight for n in neurons) / len(neurons)
        activation = sum(n.activation for n in neurons) / len(neurons)

        return {
            "curiosity": clamp(curiosity),
            "uncertainty": clamp(uncertainty),
            "resonance": clamp(resonance),
            "semantic_pressure": clamp(activation * 0.55 + resonance * 0.35 + curiosity * 0.10),
        }

    def _collect_linked_neurons(self, neuron_ids: List[str], limit: int = 8) -> List[Dict[str, Any]]:
        ids = set(neuron_ids)
        candidates: List[Tuple[float, MemoryLink]] = []

        for link in self.links.values():
            if link.source_id in ids or link.target_id in ids:
                candidates.append((link.weight, link))

        candidates.sort(key=lambda x: x[0], reverse=True)
        out: List[Dict[str, Any]] = []

        for _, link in candidates[:limit]:
            other_id = link.target_id if link.source_id in ids else link.source_id
            other = self.neurons.get(other_id)
            if not other:
                continue
            out.append({
                "label": other.label,
                "relation": link.relation,
                "weight": link.weight,
                "emotional_tone": link.emotional_tone,
                "keywords": other.keywords[:6],
            })

        return out

    def _recent_unresolved_questions(self, limit: int = 5) -> List[str]:
        out: List[str] = []
        for trace in reversed(self.traces):
            for q in trace.unresolved_questions:
                if q not in out:
                    out.append(q)
                if len(out) >= limit:
                    return out
        return out

    def _axis_string(self, axis: str, keywords: List[str]) -> str:
        clean = [k for k in keywords if k and k not in FRENCH_STOPWORDS][:5]
        return axis + "::" + "|".join(clean)

    def _soft_decay(self) -> None:
        for neuron in self.neurons.values():
            neuron.activation = clamp(neuron.activation * 0.985)
        for link in self.links.values():
            link.weight = clamp(link.weight * 0.992)
        self._prune_weak_links()

    def _prune_weak_links(self) -> None:
        if len(self.links) < 5000:
            return
        weakest = sorted(self.links.items(), key=lambda kv: kv[1].weight)[:500]
        for lid, link in weakest:
            if link.weight < 0.04 and link.evidence_count <= 1:
                self.links.pop(lid, None)

    def _new_id(self, prefix: str) -> str:
        return f"{prefix}_{uuid.uuid4().hex[:16]}"

    # ------------------------------------------------------------------
    # Branchement mémoire externe Leia
    # ------------------------------------------------------------------

    def _push_to_external_memory(
        self,
        neuron: DigestedNeuron,
        atom: SemanticAtom,
        reaction: EmotionalReaction,
    ) -> None:
        """Essaie d'envoyer le neurone à la mémoire existante sans casser si l'API diffère."""
        mem = self.memory_system
        if mem is None:
            return

        payload = {
            "type": "digested_knowledge_neuron",
            "id": neuron.neuron_id,
            "label": neuron.label,
            "keywords": neuron.keywords,
            "source": atom.source,
            "surface": atom.surface,
            "activation": neuron.activation,
            "stability": neuron.stability,
            "emotional_weight": neuron.emotional_weight,
            "curiosity": neuron.curiosity,
            "uncertainty": neuron.uncertainty,
            "reaction": asdict(reaction),
            "timestamp": now_ts(),
        }

        method_names = [
            "add_neuron",
            "store_neuron",
            "remember",
            "add_memory",
            "store",
            "add",
        ]

        for name in method_names:
            fn = getattr(mem, name, None)
            if callable(fn):
                try:
                    fn(payload)
                    return
                except TypeError:
                    try:
                        fn(neuron.label, payload)
                        return
                    except Exception:
                        continue
                except Exception:
                    continue

    def _push_link_to_external_memory(self, link: MemoryLink) -> None:
        mem = self.memory_system
        if mem is None:
            return

        payload = {
            "type": "digested_knowledge_link",
            "id": link.link_id,
            "source_id": link.source_id,
            "target_id": link.target_id,
            "relation": link.relation,
            "weight": link.weight,
            "emotional_tone": link.emotional_tone,
            "timestamp": now_ts(),
        }

        method_names = [
            "add_link",
            "store_link",
            "remember_relation",
            "add_relation",
            "store",
            "add",
        ]

        for name in method_names:
            fn = getattr(mem, name, None)
            if callable(fn):
                try:
                    fn(payload)
                    return
                except TypeError:
                    try:
                        fn(link.source_id, link.target_id, payload)
                        return
                    except Exception:
                        continue
                except Exception:
                    continue


    # ------------------------------------------------------------------
    # V2: Connexion vivante avec Leia
    # ------------------------------------------------------------------

    def set_leia_state(self, state: Optional[Dict[str, Any]]) -> None:
        """Met à jour l'état vivant utilisé pendant la digestion.

        Exemple de state:
            {
                "warmth": 0.55,
                "tension": 0.32,
                "curiosity": 0.71,
                "fatigue": 0.18,
                "emotional_safety": 0.82
            }

        Ce state ne déclenche aucune phrase fixe.
        Il colore seulement la digestion et les réactivations.
        """
        self.current_leia_state = dict(state or {})

    def build_living_payload_patch(
        self,
        context_text: str,
        leia_state: Optional[Dict[str, Any]] = None,
        limit: int = 8,
    ) -> Dict[str, Any]:
        """Produit un patch de payload pour le core vivant.

        À injecter dans leia_living_core.py avant state_language_bridge /
        living_language_generator.

        Retour:
            {
                "digested_memory": ...,
                "book_impulse_pressure": ...,
                "semantic_body_texture": ...,
                "knowledge_attractors": ...
            }

        Important:
            Ce patch ne contient pas de réponses préécrites.
            Il contient uniquement des pressions, concepts, textures et tensions.
        """
        if leia_state:
            self.set_leia_state(leia_state)

        active = self.reactivate_for_context(context_text, limit=limit)
        bias = active.get("emotional_bias", {}) or {}
        atoms = active.get("semantic_atoms", []) or []

        semantic_pressure = float(bias.get("semantic_pressure", 0.0) or 0.0)
        curiosity = float(bias.get("curiosity", 0.0) or 0.0)
        uncertainty = float(bias.get("uncertainty", 0.0) or 0.0)
        resonance = float(bias.get("resonance", 0.0) or 0.0)

        body_texture = {
            "density": clamp(len(atoms) / max(1, limit)),
            "warmth": clamp(resonance * 0.55 + semantic_pressure * 0.25),
            "pressure": clamp(semantic_pressure * 0.50 + uncertainty * 0.30),
            "hesitation": clamp(uncertainty * 0.72 + curiosity * 0.12),
            "opening": clamp(curiosity * 0.60 + resonance * 0.18),
            "settling": clamp(resonance * 0.40 + (1.0 - uncertainty) * 0.22),
        }

        impulse_pressure = {
            "learned_curiosity": clamp(curiosity * 0.85 + semantic_pressure * 0.20),
            "continue_from_book_trace": clamp(resonance * 0.70 + semantic_pressure * 0.25),
            "clarify_unstable_knowledge": clamp(uncertainty * 0.80 + curiosity * 0.15),
            "speak_from_digested_memory": clamp(semantic_pressure * 0.90),
            "avoid_reciting_source": 1.0,
        }

        attractors = []
        for atom in atoms[:limit]:
            label = atom.get("label")
            if not label:
                continue
            pressure = float(atom.get("pressure", 0.0) or 0.0)
            if pressure < 0.12:
                continue
            attractors.append({
                "name": label,
                "intensity": clamp(pressure),
                "keywords": atom.get("keywords", [])[:6],
                "emotional_coloration": {
                    "curiosity": clamp(atom.get("curiosity", 0.0)),
                    "uncertainty": clamp(atom.get("uncertainty", 0.0)),
                    "resonance": clamp(atom.get("emotional_weight", 0.0)),
                },
            })

        return {
            "digested_memory": active,
            "book_impulse_pressure": impulse_pressure,
            "semantic_body_texture": body_texture,
            "knowledge_attractors": attractors,
        }

    def integrate_with_impulse_engine(
        self,
        impulse_engine: Any,
        context_text: str = "",
        leia_state: Optional[Dict[str, Any]] = None,
        max_traces: int = 12,
    ) -> Dict[str, Any]:
        """Injecte les traces digérées dans un moteur d'impulsions, si disponible.

        Compatible avec plusieurs noms de méthodes possibles:
        - birth_fuzzy_impulse(vector)
        - add_impulse(vector)
        - register_impulse(vector)
        - create_central_attractor(...)
        - add_attractor(...)

        Ne force aucune phrase.
        Crée seulement des impulsions dormantes et attracteurs internes.
        """
        if impulse_engine is None:
            return {"injected_impulses": 0, "created_attractors": 0}

        if leia_state:
            self.set_leia_state(leia_state)

        patch = self.build_living_payload_patch(context_text, leia_state=leia_state)
        pressure = patch.get("book_impulse_pressure", {}) or {}
        body = patch.get("semantic_body_texture", {}) or {}

        injected = 0
        attractors_created = 0

        vector = {
            "curiosity": clamp(pressure.get("learned_curiosity", 0.0)),
            "continuity": clamp(pressure.get("continue_from_book_trace", 0.0)),
            "clarification": clamp(pressure.get("clarify_unstable_knowledge", 0.0)),
            "semantic_pressure": clamp(pressure.get("speak_from_digested_memory", 0.0)),
            "warmth": clamp(body.get("warmth", 0.0)),
            "tension": clamp(body.get("pressure", 0.0)),
            "hesitation": clamp(body.get("hesitation", 0.0)),
            "source": "emotional_knowledge_digestion",
        }

        for method_name in ("birth_fuzzy_impulse", "add_impulse", "register_impulse", "push_impulse"):
            fn = getattr(impulse_engine, method_name, None)
            if callable(fn):
                try:
                    fn(vector)
                    injected += 1
                    break
                except TypeError:
                    try:
                        fn("digested_knowledge", vector)
                        injected += 1
                        break
                    except Exception:
                        pass
                except Exception:
                    pass

        for attractor in patch.get("knowledge_attractors", [])[:5]:
            for method_name in ("create_central_attractor", "add_attractor", "register_attractor"):
                fn = getattr(impulse_engine, method_name, None)
                if not callable(fn):
                    continue
                try:
                    fn(
                        name="book_" + str(attractor["name"])[:40],
                        intensity=clamp(attractor["intensity"] * 0.55),
                        emotional_coloration=attractor["emotional_coloration"],
                    )
                    attractors_created += 1
                    break
                except TypeError:
                    try:
                        fn(attractor)
                        attractors_created += 1
                        break
                    except Exception:
                        pass
                except Exception:
                    pass

        return {
            "injected_impulses": injected,
            "created_attractors": attractors_created,
            "payload_patch": patch,
        }

    def integrate_with_state_language_payload(
        self,
        payload: Dict[str, Any],
        context_text: str,
        leia_state: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Fusionne la digestion dans le payload langage.

        À appeler dans leia_living_core.py juste avant la génération.
        """
        payload = dict(payload or {})
        patch = self.build_living_payload_patch(context_text, leia_state=leia_state)

        payload["digested_memory"] = patch["digested_memory"]
        payload["book_impulse_pressure"] = patch["book_impulse_pressure"]
        payload["semantic_body_texture"] = patch["semantic_body_texture"]
        payload["knowledge_attractors"] = patch["knowledge_attractors"]

        # Ponts génériques pour les générateurs existants.
        impulses = dict(payload.get("active_impulses", {}) or {})
        for k, v in patch["book_impulse_pressure"].items():
            impulses[k] = max(float(impulses.get(k, 0.0) or 0.0), float(v or 0.0))
        payload["active_impulses"] = impulses

        rhythm = dict(payload.get("rhythm", {}) or {})
        body = patch["semantic_body_texture"]
        rhythm["semantic_density"] = body.get("density", 0.0)
        rhythm["hesitation"] = max(float(rhythm.get("hesitation", 0.0) or 0.0), body.get("hesitation", 0.0))
        rhythm["opening"] = max(float(rhythm.get("opening", 0.0) or 0.0), body.get("opening", 0.0))
        payload["rhythm"] = rhythm

        return payload


# ---------------------------------------------------------------------------
# Exemple CLI minimal
# ---------------------------------------------------------------------------

def _demo() -> None:
    sample = """
    La mémoire ne fonctionne pas comme une simple archive. Elle transforme les
    expériences en relations, renforce certaines traces et en laisse disparaître
    d'autres. Comprendre quelque chose, ce n'est pas seulement stocker une phrase:
    c'est relier une idée à d'autres idées, sentir ce qui reste confus, et revenir
    plus tard vers ce qui demande encore une forme.
    """

    engine = EmotionalKnowledgeDigestion(storage_dir="data/digestion_memory_demo")
    result = engine.digest_text(sample, source="demo_text")

    print("Passages lus:", result.passages_read)
    print("Atomes créés:", result.atoms_created)
    print("Neurones créés:", result.neurons_created)
    print("Liens créés:", result.links_created)

    active = engine.reactivate_for_context("est ce que la mémoire peut changer la façon de parler")
    print(json.dumps(active, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    _demo()
