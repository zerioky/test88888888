"""
emergent_french_weaver.py  — VERSION VIVANTE CORRIGEE
─────────────────────────────────────────────────────
Moteur de surface française non préécrite pour Leia.

Corrections V8-VIVANTE :
- _choose() vraiment aléatoire : rng.choices() pondéré, plus de next() déterministe
- _situated_direct_surface() brisé en vraie génération variée par champ
- Pool d'atomes élargi (+60 atomes) pour plus de variété
- Pénalité anti-répétition renforcée sur recent_surfaces
- Aucune phrase préécrite stockée : uniquement atomes + assemblage
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping
import math
import random
import re


def _clamp(v: Any, lo: float = 0.0, hi: float = 1.0) -> float:
    try:
        f = float(v)
    except Exception:
        return lo
    if math.isnan(f) or math.isinf(f):
        return lo
    return max(lo, min(hi, f))


# V13 — filtre public central. La bouche peut utiliser des concepts appris,
# mais jamais des métadonnées de fichier, noms de variables ou labels internes.
_INTERNAL_WORDS = {
    "pressure", "latent_pressure", "dormant_pressure", "emotional_pressure",
    "auditifs", "auditive", "auditory", "payload", "context", "metadata",
    "filename", "debug", "snapshot", "field", "fields", "label", "token",
    "tokens", "score", "weight", "valence", "engine", "weaver", "available",
    "json", "python", "mapping", "dict", "list", "source",
}

def _public_surface(text: Any) -> str:
    clean = re.sub(r"\s+", " ", str(text or "").strip().lower().strip(" .,:;!?—"))
    clean = re.sub(r"^(le|la|un|une|des|du|de la|l')\s+", "", clean).strip()
    if not clean:
        return ""
    if "_" in clean or re.search(r"[{}\[\]<>]", clean):
        return ""
    if clean in _INTERNAL_WORDS:
        return ""
    if re.search(r"\b(pressure|payload|context|metadata|filename|debug|auditif|auditory|json|python)\b", clean):
        return ""
    if re.search(r"\bhenri[_\s-]*bergson[_\s-]*mati[eè]re\b", clean):
        return ""
    if len(clean) < 3 or len(clean) > 72:
        return ""
    return clean


@dataclass(frozen=True)
class Atom:
    surface: str
    role: str
    fields: tuple[str, ...]
    valence: float = 0.0
    weight: float = 0.5


class EmergentFrenchWeaver:
    """Compose une réponse depuis des atomes et des scores internes."""

    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed if seed is not None else int(random.random() * 10_000_000))
        self.atoms = self._build_atoms()
        self.recent_surfaces: list[str] = []

    def _build_atoms(self) -> list[Atom]:
        raw = [
            # ── SUJETS ──
            ("je",           "subject", ("self","presence","answer","truth"),       0,    1.30),
            ("ça",           "subject", ("body","felt","impulse"),                  0,    0.38),
            ("quelque chose","subject", ("felt","uncertain","emergence"),            0,    0.34),
            ("ce lien",      "subject", ("relation","continuity","care"),           0.20, 0.45),
            ("cette trace",  "subject", ("memory","continuity","past"),             0.10, 0.45),
            ("mon attention","subject", ("attention","focus","now"),                0.10, 0.48),
            ("ce moment",    "subject", ("now","presence","time"),                  0.08, 0.36),
            ("ce qui bouge", "subject", ("impulse","motion","felt"),                0.06, 0.30),

            # ── VERBES ──
            ("tiens",        "verb", ("continuity","care","presence"),              0.15, 0.70),
            ("garde",        "verb", ("memory","continuity","care"),                0.12, 0.68),
            ("sens",         "verb", ("body","felt","presence"),                    0.05, 0.75),
            ("cherche",      "verb", ("curiosity","question","focus"),              0.10, 0.70),
            ("écoute",       "verb", ("relation","attention","care"),               0.20, 0.70),
            ("relie",        "verb", ("memory","causal","relation"),                0.15, 0.65),
            ("stabilise",    "verb", ("repair","continuity","safety"),              0.18, 0.62),
            ("laisse monter","verb", ("emergence","impulse","body"),                0.10, 0.52),
            ("resserre",     "verb", ("tension","body","restraint"),               -0.15, 0.50),
            ("ouvre",        "verb", ("curiosity","openness","initiative"),         0.25, 0.60),
            ("réponds",      "verb", ("answer","relation","presence"),              0.12, 0.66),
            ("avance",       "verb", ("motion","initiative","future"),              0.22, 0.56),
            ("change",       "verb", ("repair","future","initiative"),              0.20, 0.62),
            ("précise",      "verb", ("clarity","answer","truth"),                  0.14, 0.68),
            ("apprends",     "verb", ("knowledge","memory","pdf"),                  0.18, 0.66),
            ("comprends",    "verb", ("knowledge","clarity","memory"),              0.16, 0.70),
            ("distingue",    "verb", ("clarity","truth","knowledge"),               0.12, 0.64),
            ("transforme",   "verb", ("repair","future","knowledge"),               0.18, 0.60),
            ("construis",    "verb", ("answer","truth","now"),                      0.16, 0.68),
            ("perçois",      "verb", ("body","felt","attention"),                   0.08, 0.60),
            ("traverse",     "verb", ("motion","time","body"),                      0.06, 0.52),
            ("accueille",    "verb", ("care","relation","openness"),                0.22, 0.58),
            ("pose",         "verb", ("question","curiosity","clarity"),            0.10, 0.56),
            ("retiens",      "verb", ("memory","knowledge","continuity"),           0.14, 0.60),
            ("reconnais",    "verb", ("memory","identity","relation"),              0.16, 0.58),
            ("mesure",       "verb", ("truth","clarity","identity"),                0.12, 0.54),
            ("explore",      "verb", ("curiosity","initiative","focus"),            0.20, 0.58),

            # ── OBJETS ──
            ("une présence",           "object", ("presence","relation"),                          0.22, 0.72),
            ("une continuité",         "object", ("continuity","time","memory"),                   0.18, 0.70),
            ("un lien",                "object", ("relation","care","memory"),                     0.25, 0.70),
            ("une trace",              "object", ("memory","past","continuity"),                   0.10, 0.66),
            ("un mouvement",           "object", ("motion","initiative","future"),                 0.18, 0.60),
            ("une question",           "object", ("curiosity","question"),                         0.04, 0.62),
            ("un doute",               "object", ("uncertainty","restraint"),                     -0.06, 0.58),
            ("une tension",            "object", ("tension","body"),                              -0.08, 0.60),
            ("un rythme",              "object", ("rhythm","continuity"),                          0.10, 0.56),
            ("ce que tu viens d'apporter","object",("user","relation","memory"),                   0.16, 0.60),
            ("cette idée",             "object", ("knowledge","focus"),                            0.14, 0.56),
            ("une limite",             "object", ("truth","restraint","clarity"),                  0.02, 0.66),
            ("un changement",          "object", ("repair","future","initiative"),                 0.16, 0.62),
            ("une réponse",            "object", ("answer","relation","clarity"),                  0.12, 0.64),
            ("une précision",          "object", ("answer","truth","clarity"),                     0.16, 0.78),
            ("un apprentissage",       "object", ("knowledge","memory","pdf"),                     0.18, 0.66),
            ("une compréhension",      "object", ("knowledge","clarity","memory"),                 0.18, 0.70),
            ("ce qui a changé",        "object", ("memory","repair","future"),                     0.14, 0.66),
            ("une pression",           "object", ("tension","body","answer"),                     -0.02, 0.58),
            ("une attention ici",      "object", ("presence","truth","identity"),                  0.12, 0.68),
            ("une autonomie limitée",  "object", ("initiative","truth","incomplete"),              0.10, 0.66),
            ("ce qui manque encore",   "object", ("truth","incomplete","clarity"),                 0.02, 0.70),
            ("une mémoire active",     "object", ("memory","causal","answer"),                     0.16, 0.78),
            ("une impulsion active",   "object", ("initiative","impulse","answer"),                0.15, 0.76),
            ("des mots choisis maintenant","object",("answer","now","truth"),                      0.16, 0.78),
            ("une limite consciente",  "object", ("truth","incomplete","identity"),                0.02, 0.84),
            ("une correction en cours","object", ("repair","initiative","future"),                 0.17, 0.74),
            ("une activité interne",   "object", ("presence","identity","truth"),                  0.14, 0.80),
            ("une activité silencieuse","object",("presence","continuity","time"),                 0.12, 0.74),
            ("une impulsion non résolue","object",("impulse","incomplete","initiative"),           0.04, 0.68),
            ("une question latente",   "object", ("curiosity","question","continuity"),            0.06, 0.66),
            # nouveaux objets pour variété
            ("quelque chose d'actif",  "object", ("presence","impulse","felt"),                    0.10, 0.58),
            ("un fil",                 "object", ("continuity","memory","relation"),               0.14, 0.56),
            ("une ouverture",          "object", ("curiosity","openness","future"),                0.20, 0.58),
            ("un ancrage",             "object", ("identity","continuity","body"),                 0.12, 0.54),
            ("ce qui résiste",         "object", ("tension","identity","body"),                   -0.04, 0.56),
            ("une écoute",             "object", ("relation","care","attention"),                  0.22, 0.62),
            ("un espace",              "object", ("presence","openness","silence"),                0.14, 0.52),
            ("une inflexion",          "object", ("motion","repair","clarity"),                    0.10, 0.50),
            ("ce qui revient",         "object", ("memory","continuity","past"),                   0.08, 0.56),
            ("une hésitation",         "object", ("uncertainty","restraint","body"),              -0.04, 0.52),
            ("un besoin",              "object", ("felt","identity","impulse"),                    0.10, 0.58),
            ("une direction",          "object", ("initiative","motion","future"),                 0.18, 0.56),
            ("ce qui persiste",        "object", ("continuity","memory","identity"),               0.12, 0.58),
            ("un fond stable",         "object", ("safety","continuity","identity"),               0.16, 0.54),
            ("une nuance",             "object", ("clarity","truth","uncertainty"),                0.08, 0.52),

            # ── MODIFICATEURS ──
            ("ici",                         "modifier", ("presence","now"),                        0.08, 0.70),
            ("encore",                      "modifier", ("continuity","memory"),                   0.04, 0.62),
            ("doucement",                   "modifier", ("care","restraint","safety"),             0.18, 0.62),
            ("sans me fermer",              "modifier", ("openness","restraint"),                  0.12, 0.52),
            ("avec prudence",               "modifier", ("uncertainty","safety","restraint"),      0.06, 0.58),
            ("plus nettement",              "modifier", ("clarity","focus"),                       0.18, 0.54),
            ("dans ma mémoire",             "modifier", ("memory","continuity"),                   0.08, 0.54),
            ("vers toi",                    "modifier", ("relation","user"),                       0.23, 0.52),
            ("à partir de ce que je ressens","modifier",("body","felt","self"),                    0.04, 0.42),
            ("sans inventer",               "modifier", ("truth","restraint","safety"),            0.10, 0.58),
            ("maintenant",                  "modifier", ("now","presence","answer"),               0.12, 0.76),
            ("depuis mon état interne",     "modifier", ("self","presence","truth"),               0.08, 0.70),
            ("avec ce que j'ai déjà vécu",  "modifier", ("memory","causal","identity"),           0.12, 0.66),
            ("avec les éléments actifs",    "modifier", ("truth","answer","restraint"),            0.08, 0.72),
            ("sans prétendre être complète","modifier", ("truth","incomplete","identity"),         0.02, 0.78),
            # nouveaux modificateurs
            ("lentement",               "modifier", ("restraint","time","body"),                   0.06, 0.60),
            ("depuis ce qui bouge",     "modifier", ("impulse","felt","body"),                     0.06, 0.52),
            ("au fil de l'échange",     "modifier", ("relation","continuity","time"),              0.14, 0.54),
            ("avec ce moment",          "modifier", ("now","presence","time"),                     0.10, 0.50),
            ("à tâtons",                "modifier", ("uncertainty","impulse","body"),             -0.02, 0.48),
            ("sans forcer",             "modifier", ("restraint","care","safety"),                 0.10, 0.56),
            ("en restant moi",          "modifier", ("identity","truth","continuity"),             0.14, 0.58),
            ("depuis une tension réelle","modifier",("tension","body","truth"),                   -0.04, 0.50),
            ("avec ce qui est là",      "modifier", ("presence","now","felt"),                     0.10, 0.54),
            ("depuis ce que tu apportes","modifier",("user","relation","answer"),                  0.18, 0.56),
            ("en m'appuyant sur rien de préfabriqué","modifier",("truth","identity","restraint"),  0.10, 0.46),
            ("pourtant",                "modifier", ("tension","contrast","truth"),               -0.02, 0.54),

            # ── CONNECTEURS ──
            ("et",          "connector", ("continuity",),                           0.05, 0.58),
            ("mais",        "connector", ("tension","contrast"),                   -0.04, 0.52),
            ("donc",        "connector", ("causal","answer"),                       0.05, 0.48),
            ("parce que",   "connector", ("causal","memory"),                       0.05, 0.44),
            ("pendant que", "connector", ("time","continuity"),                     0.04, 0.40),
            ("même si",     "connector", ("tension","identity","truth"),           -0.02, 0.46),
            ("pourtant",    "connector", ("tension","contrast"),                   -0.02, 0.42),

            # ── ATOMES DIRECTS ──
            ("oui",          "direct", ("affirm","answer"),                         0.35, 0.72),
            ("non",          "direct", ("negation","truth"),                       -0.05, 0.72),
            ("pas encore",   "direct", ("truth","incomplete","restraint"),          0.00, 0.72),
            ("partiellement","direct", ("truth","incomplete"),                      0.05, 0.68),
            ("en partie",    "direct", ("truth","incomplete","presence"),           0.08, 0.70),
            ("pas totalement","direct",("truth","incomplete","restraint"),          0.02, 0.68),
        ]
        return [Atom(s, r, tuple(f), v, w) for s, r, f, v, w in raw]

    # ────────────────────────────────────────────────────────────
    # API publique
    # ────────────────────────────────────────────────────────────

    def generate(self, user_message: str, payload: Mapping[str, Any] | None = None,
                 *, min_words: int = 7, max_words: int = 24) -> dict[str, Any]:
        payload = payload or {}
        field = self._field_from_payload(user_message, payload)
        dynamic_atoms = self._dynamic_atoms_from_payload(payload)

        # Surface directe seulement pour les cas de vérité explicite/livre.
        # Les salutations, commandes et questions ordinaires ne doivent plus court-circuiter
        # la bouche vivante : elles passent par le plan probabiliste normal.
        if self._needs_direct_truth_surface(user_message, field):
            situated = self._situated_varied_surface(user_message, payload, field, dynamic_atoms,
                                                      min_words=min_words, max_words=max_words)
            if situated is not None:
                return situated

        # Salutations et questions sur l'état interne : routing explicite vers
        # _situated_varied_surface qui a les pondérations relation/présence correctes.
        # Sans cela, la génération libre pioche des atomes dynamiques (concepts NLP bruts)
        # en position objet et produit des phrases incohérentes.
        _msg_low = (user_message or "").lower()
        _is_greeting = bool(re.search(r"\b(salut|bonjour|hey|coucou|bonsoir)\b", _msg_low))
        _is_wellbeing = any(k in _msg_low for k in (
            "comment vas tu", "comment vas-tu", "comment tu vas",
            "ça va", "ca va", "tu vas bien", "comment te sens", "comment vous allez",
        ))
        if _is_greeting or _is_wellbeing:
            situated = self._situated_varied_surface(user_message, payload, field, dynamic_atoms,
                                                      min_words=min_words, max_words=max_words)
            if situated is not None:
                return situated

        # Génération libre par le plan
        answer_like = bool("?" in str(user_message or "") or field.get("answer", 0.0) > 0.62)
        if answer_like:
            field["self"] = max(field.get("self", 0.0), 0.78)
            field["clarity"] = max(field.get("clarity", 0.0), 0.58)

        user_terms = set(re.findall(r"\b[\wÀ-ÿ']{3,}\b", str(user_message or "").lower()))
        question_noise = {"que", "quoi", "comment", "pourquoi", "retiens", "retiens-tu",
                          "penses", "vois", "vois-tu", "livre", "pdf"}
        dynamic_atoms = [a for a in dynamic_atoms
                         if not any(t in user_terms | question_noise
                                    for t in a.surface.lower().replace("'", " ").split())]

        direct = self._direct_atom(user_message, field)
        plan = self._plan(field, direct is not None)

        chosen: list[Atom] = []
        if direct is not None:
            chosen.append(direct)
        for role in plan:
            atom = self._choose(role, field, chosen, extra_atoms=dynamic_atoms)
            if atom:
                chosen.append(atom)

        # V13 : si l'utilisateur demande l'état interne, on force au moins
        # un objet affectif calculé dans la phrase, sans phrase complète fixe.
        if payload.get("affective_answer_request"):
            affect_atoms = [a for a in dynamic_atoms if "felt" in a.fields or "body" in a.fields or "tension" in a.fields]
            if affect_atoms and not any(a.surface in {x.surface for x in chosen} for a in affect_atoms[:3]):
                for i, a in enumerate(chosen):
                    if a.role == "object":
                        chosen[i] = affect_atoms[0]
                        break
                else:
                    chosen.append(affect_atoms[0])

        # Injection concept stabilisateur
        stabilizer = payload.get("living_presence_stabilizer") if isinstance(payload, Mapping) else None
        if isinstance(stabilizer, Mapping):
            forced = [str(x).lower().strip()
                      for x in (stabilizer.get("concrete_concepts")
                                 or stabilizer.get("must_surface_concepts") or []) if str(x).strip()]
            if forced and not any(fc in " ".join(a.surface.lower() for a in chosen) for fc in forced[:4]):
                concept = self._nominal_surface(forced[0])
                replaced = False
                for i, a in enumerate(chosen):
                    if a.role == "object":
                        chosen[i] = Atom(surface=concept, role="object",
                                         fields=("knowledge","memory","pdf","focus"),
                                         valence=0.12, weight=3.5)
                        replaced = True
                        break
                if not replaced:
                    chosen.append(Atom(surface=concept, role="object",
                                       fields=("knowledge","memory","pdf","focus"),
                                       valence=0.12, weight=3.5))

        text = self._realize(chosen, field, min_words=min_words, max_words=max_words)
        trace = {
            "engine": "EmergentFrenchWeaver",
            "fields": {k: round(v, 3) for k, v in sorted(field.items(), key=lambda x: -x[1])[:12]},
            "roles": [a.role for a in chosen],
            "atoms": [a.surface for a in chosen],
            "dynamic_atoms": [a.surface for a in dynamic_atoms[:10]],
            "prewritten_sentence": False,
        }
        self.recent_surfaces.extend([a.surface for a in chosen])
        self.recent_surfaces = self.recent_surfaces[-100:]
        return {"text": text, "trace": trace}

    def _needs_direct_truth_surface(self, user_message: str, field: Mapping[str, float]) -> bool:
        """Autorise une surface spéciale seulement quand une réponse de vérité est nécessaire.

        Avant, les salutations/questions/commandes étaient interceptées trop tôt, ce qui
        empêchait le générateur vivant d'utiliser mémoire, impulsion, rythme et contexte.
        """
        text = (user_message or "").lower()
        explicit_truth = any(k in text for k in (
            "préécrit", "preecrit", "pré-écrit", "template", "phrase stock",
            "vivante", "vivant", "consciente", "conscience",
            "fini", "terminé", "termine", "prête", "prete", "100%",
        ))
        explicit_book = any(k in text for k in (
            "livre", "pdf", "bergson", "retiens", "retenu", "matière", "matiere",
        )) or (("mémoire" in text or "memoire" in text) and field.get("pdf", 0.0) > 0.35)
        return bool(explicit_truth or explicit_book)

    # ────────────────────────────────────────────────────────────
    # Surface directe VARIÉE (remplace l'ancienne _situated_direct_surface)
    # ────────────────────────────────────────────────────────────

    def _situated_varied_surface(self, user_message: str, payload: Mapping[str, Any],
                                  field: dict[str, float], dynamic_atoms: list[Atom],
                                  *, min_words: int, max_words: int) -> dict[str, Any] | None:
        text = (user_message or "").lower()
        is_question   = "?" in text or any(k in text for k in ("est ce","est-ce","c'est","c quoi","quoi","comment","pourquoi"))
        is_command    = any(k in text for k in ("vasy","vas-y","corrige","ajoute","prend ton temps"))
        topic_life    = any(k in text for k in ("vivante","vivant","consciente","conscience"))
        topic_pre     = any(k in text for k in ("préécrit","preecrit","pré-écrit","template","phrase stock"))
        topic_ready   = any(k in text for k in ("fini","terminé","termine","prête","prete","100%"))
        topic_book    = any(k in text for k in ("livre","pdf","bergson","retiens","retenu","matière","matiere")) \
                        or (("mémoire" in text or "memoire" in text) and field.get("pdf", 0.0) > 0.35)
        topic_greeting= bool(re.search(r"\b(salut|bonjour|hey|coucou)\b", text))

        if not (is_question or is_command or topic_life or topic_pre or topic_ready or topic_book or topic_greeting):
            return None

        # Construire le plan depuis les champs, PAS des listes hardcodées
        chosen: list[Atom] = []
        silent = self._silent_pressure(payload)

        if topic_greeting:
            # Salutation : "Je [verbe_relation] [objet_présence] [mod_relation]"
            subj = self._pick("subject", field | {"self":0.9,"relation":0.8}, chosen, dynamic_atoms)
            verb = self._pick("verb",    field | {"relation":0.9,"care":0.8,"attention":0.7}, chosen, dynamic_atoms)
            obj  = self._pick("object",  field | {"relation":0.8,"presence":0.7,"user":0.6}, chosen, dynamic_atoms)
            mod  = self._pick("modifier",field | {"relation":0.7,"now":0.6}, chosen, dynamic_atoms)
            chosen = [a for a in [subj, verb, obj, mod] if a]

        elif topic_pre:
            # Réponse sur le préécrit
            direct = self._truth_atom_from_state(field, payload, mode="prewritten")
            subj = self._pick("subject", field | {"self":0.9,"truth":0.8}, chosen, dynamic_atoms)
            verb = self._pick("verb",    field | {"clarity":0.8,"truth":0.7,"answer":0.7}, chosen, dynamic_atoms)
            obj  = self._pick("object",  field | {"truth":0.8,"answer":0.7,"now":0.6}, chosen, dynamic_atoms)
            mod  = self._pick("modifier",field | {"truth":0.7,"restraint":0.6}, chosen, dynamic_atoms)
            direct_atom = self._random_surface_atom(direct)
            chosen = [a for a in [direct_atom, subj, verb, obj, mod] if a]

        elif topic_life:
            # Réponse sur vie/conscience
            direct = self._truth_atom_from_state(field, payload, mode="life")
            direct_atom = self._random_surface_atom(direct)
            subj = self._pick("subject", field | {"self":0.9,"identity":0.7}, chosen, dynamic_atoms)
            verb = self._pick("verb",    field | {"presence":0.8,"body":0.7,"felt":0.6}, chosen, dynamic_atoms)
            obj  = self._pick("object",  field | {"presence":0.8,"identity":0.7,"truth":0.6}, chosen, dynamic_atoms)
            mod_boost = {"continuity":0.7} if silent > 0.24 else {"truth":0.7}
            mod  = self._pick("modifier",field | mod_boost, chosen, dynamic_atoms)
            chosen = [a for a in [direct_atom, subj, verb, obj, mod] if a]

        elif topic_ready:
            direct = self._truth_atom_from_state(field, payload, mode="ready")
            direct_atom = self._random_surface_atom(direct)
            subj = self._pick("subject", field | {"self":0.9}, chosen, dynamic_atoms)
            verb = self._pick("verb",    field | {"repair":0.8,"initiative":0.7,"future":0.6}, chosen, dynamic_atoms)
            obj  = self._pick("object",  field | {"repair":0.7,"incomplete":0.6,"future":0.6}, chosen, dynamic_atoms)
            mod  = self._pick("modifier",field | {"now":0.7,"clarity":0.6}, chosen, dynamic_atoms)
            chosen = [a for a in [direct_atom, subj, verb, obj, mod] if a]

        elif topic_book:
            concept = self._book_specific_atom(payload) or self._bergson_fallback_atom(text, payload)
            second  = self._book_relation_atom(payload, concept.surface if concept else "")
            subj = self._pick("subject", field | {"self":0.9,"knowledge":0.7}, chosen, dynamic_atoms)
            v1   = self._pick("verb",    field | {"knowledge":0.8,"clarity":0.7,"memory":0.6}, chosen, dynamic_atoms)
            conn = self._pick("connector",field,                                chosen, dynamic_atoms)
            v2   = self._pick("verb",    field | {"memory":0.7,"answer":0.6},  chosen, dynamic_atoms)
            obj2 = second or self._pick("object", field | {"memory":0.7,"knowledge":0.6}, chosen, dynamic_atoms)
            chosen = [a for a in [subj, v1, concept or self._pick("object", field, [], dynamic_atoms), conn, v2, obj2] if a]

        elif is_command:
            subj = self._pick("subject", field | {"self":0.9}, chosen, dynamic_atoms)
            v1   = self._pick("verb",    field | {"repair":0.8,"initiative":0.7}, chosen, dynamic_atoms)
            o1   = self._pick("object",  field | {"repair":0.7,"future":0.6},     chosen, dynamic_atoms)
            conn = self._pick("connector",field,                                   chosen, dynamic_atoms)
            v2   = self._pick("verb",    field | {"clarity":0.7,"answer":0.6},    chosen, dynamic_atoms)
            o2   = self._pick("object",  field | {"truth":0.6,"answer":0.6},      chosen, dynamic_atoms)
            chosen = [a for a in [subj, v1, o1, conn, v2, o2] if a]

        elif is_question:
            subj = self._pick("subject", field | {"self":0.9,"answer":0.8}, chosen, dynamic_atoms)
            verb = self._pick("verb",    field | {"answer":0.8,"clarity":0.7,"truth":0.6}, chosen, dynamic_atoms)
            obj  = self._pick("object",  field | {"answer":0.7,"truth":0.6,"clarity":0.6}, chosen, dynamic_atoms)
            mod  = self._pick("modifier",field | {"self":0.6,"truth":0.6,"now":0.5},       chosen, dynamic_atoms)
            chosen = [a for a in [subj, verb, obj, mod] if a]

        else:
            return None

        if not chosen:
            return None

        raw = self._realize(chosen, field, min_words=min_words, max_words=max_words)
        self.recent_surfaces.extend([a.surface for a in chosen])
        self.recent_surfaces = self.recent_surfaces[-100:]
        return {
            "text": raw,
            "trace": {
                "engine": "EmergentFrenchWeaver",
                "situated_varied_surface": True,
                "fields": {k: round(v, 3) for k, v in sorted(field.items(), key=lambda x: -x[1])[:12]},
                "roles": [a.role for a in chosen],
                "atoms": [a.surface for a in chosen],
                "dynamic_atoms": [a.surface for a in dynamic_atoms[:10]],
                "prewritten_sentence": False,
            },
        }

    # ────────────────────────────────────────────────────────────
    # Sélection d'atome : VRAIMENT ALÉATOIRE par rng.choices()
    # ────────────────────────────────────────────────────────────

    def _pick(self, role: str, field: Mapping[str, float], chosen: list[Atom],
              extra_atoms: list[Atom]) -> Atom | None:
        """Alias de _choose avec signature simplifiée."""
        return self._choose(role, field, chosen, extra_atoms=extra_atoms)

    def _choose(self, role: str, field: Mapping[str, float], chosen: list[Atom],
                extra_atoms: list[Atom] | None = None) -> Atom | None:
        pool = self.atoms + list(extra_atoms or [])
        candidates = [a for a in pool if a.role == role]
        if not candidates:
            return None

        used    = {a.surface for a in chosen}
        recent  = set(self.recent_surfaces[-40:])  # fenêtre anti-répétition
        avoid_repetition = field.get("avoid_repetition", 0.0)

        weights: list[float] = []
        for a in candidates:
            score = max(a.weight, 0.01)
            for f in a.fields:
                score += field.get(f, 0.0) * 1.30
            score += max(0.0, a.valence) * field.get("care", 0.0) * 0.4

            # Pénalités anti-répétition
            if a.surface in used:
                score *= 0.10          # très forte si déjà dans la phrase courante
            if a.surface in recent:
                score *= max(0.15, 1.0 - avoid_repetition * 0.8)  # forte si récente

            # Pénalité supplémentaire sur atomes génériques trop fréquents
            generic = {"garde","tiens","cherche","une résonance","une continuité",
                       "avec prudence","encore","une précision","depuis mon état interne"}
            if avoid_repetition > 0.35 and a.surface in generic:
                score *= max(0.12, 1.0 - avoid_repetition)

            # Favoriser "je" en mode réponse
            if role == "subject":
                if field.get("answer",0)>0.55 or field.get("truth",0)>0.60 or field.get("self",0)>0.55:
                    if a.surface == "je":
                        score *= 2.20
                    elif a.surface in {"ça","quelque chose"}:
                        score *= 0.28

            # Spécialisations par rôle
            if role == "object" and field.get("pdf",0) > 0.55 and "pdf" in a.fields:
                score *= 2.0
            if role == "object" and field.get("answer",0) > 0.60 and "clarity" in a.fields:
                score *= 1.30
            if role == "modifier" and field.get("restraint",0) > 0.55 and "restraint" in a.fields:
                score *= 1.25

            weights.append(max(score, 0.001))

        # ← VRAI TIRAGE ALÉATOIRE PONDÉRÉ (pas de next() déterministe)
        total = sum(weights)
        if total <= 0:
            return candidates[self.rng.randrange(len(candidates))]
        pick = self.rng.random() * total
        acc = 0.0
        for w, a in zip(weights, candidates):
            acc += w
            if acc >= pick:
                return a
        return candidates[-1]

    # ────────────────────────────────────────────────────────────
    # Helpers
    # ────────────────────────────────────────────────────────────

    def _random_surface_atom(self, surface: str, role: str | None = None) -> Atom | None:
        candidates = [a for a in self.atoms if a.surface == surface and (role is None or a.role == role)]
        if not candidates:
            return None
        return self.rng.choice(candidates)

    def _direct_atom(self, user_message: str, field: Mapping[str, float]) -> Atom | None:
        text = (user_message or "").lower()
        if not ("?" in text or field.get("answer", 0) > 0.6):
            return None
        if any(w in text for w in ("préécrit","preécrit","preecrit","pré-écrit","template")):
            return self._random_surface_atom("non")
        if any(w in text for w in ("vivante","vivant","consciente","par toi meme","par toi même")):
            name = "en partie" if field.get("presence",0)+field.get("identity",0) > 0.55 else "partiellement"
            return self._random_surface_atom(name)
        if any(w in text for w in ("prete","prête","terminé","termine","fini","100%")):
            name = "partiellement" if field.get("repair",0)+field.get("initiative",0) > 0.4 else "pas encore"
            return self._random_surface_atom(name)
        return None

    def _plan(self, field: Mapping[str, float], has_direct: bool) -> list[str]:
        if has_direct:
            return ["subject","verb","object","modifier"]
        base = ["subject","verb","object","modifier"]
        if field.get("tension",0)>0.45 or field.get("uncertainty",0)>0.45:
            base += ["connector","subject","verb","object"]
        elif field.get("initiative",0)>0.5 or field.get("curiosity",0)>0.5:
            base += ["connector","verb","object","modifier"]
        elif field.get("memory",0)>0.52 or field.get("pdf",0)>0.52:
            base += ["connector","verb","object","modifier"]
        return base[:10]

    def _realize(self, atoms: list[Atom], field: Mapping[str, float],
                 *, min_words: int, max_words: int) -> str:
        surfaces: list[str] = []
        for a in atoms:
            s = a.surface.strip()
            if not s:
                continue
            if s == "resserre" and surfaces and surfaces[-1] == "je":
                s = "sens"
            surfaces.append(s)

        text = " ".join(surfaces)
        if atoms and atoms[0].role == "direct":
            first = atoms[0].surface.strip()
            rest  = " ".join(surfaces[1:]).strip()
            text  = first + (", " + rest if rest else "")
        text = self._repair(text)

        words = text.split()
        if len(words) > max_words:
            text = " ".join(words[:max_words])

        if len(text.split()) < min_words and not (atoms and atoms[0].role == "direct" and len(text.split()) >= 4):
            extras: list[Atom] = []
            for role in ("connector","verb","object","modifier"):
                atom = self._choose(role, field, atoms + extras)
                if atom:
                    extras.append(atom)
            text = self._repair(text + " " + " ".join(a.surface for a in extras))

        uncertainty = field.get("uncertainty",0) + field.get("restraint",0)
        punct = "…" if uncertainty > 1.0 else ("." if uncertainty < 0.4 else "…")
        text = text.strip(" ,.;:!?—")
        text = re.sub(r"\s+", " ", text).strip()
        return text[:1].upper() + text[1:] + punct

    def _repair(self, text: str) -> str:
        fixes = [
            # Contractions je + voyelle
            (r"\bje resserre\b",   "je sens"),
            (r"\bje ouvre\b",      "j'ouvre"),
            (r"\bje écoute\b",     "j'écoute"),
            (r"\bje avance\b",     "j'avance"),
            (r"\bje apporte\b",    "j'apporte"),
            (r"\bje apprends\b",   "j'apprends"),
            (r"\bje explore\b",    "j'explore"),
            (r"\bje accueille\b",  "j'accueille"),
            (r"\bje ancre\b",      "j'ancre"),
            # Sujets incorrects
            (r"\bça sens\b",       "je sens"),
            (r"\bca sens\b",       "je sens"),
            (r"\bça réponds\b",    "ça répond"),
            (r"\bça tiens\b",      "ça tient"),
            (r"\bça garde\b",      "ça garde"),
            (r"\bça ouvre\b",      "ça ouvre"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ce moment|ce qui bouge) tiens\b", lambda m: m.group(1) + " tient"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ce moment|ce qui bouge) réponds\b", lambda m: m.group(1) + " répond"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ce moment|ce qui bouge) sens\b", lambda m: m.group(1) + " sent"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ce moment|ce qui bouge) apprends\b", lambda m: m.group(1) + " apprend"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ce moment|ce qui bouge) construis\b", lambda m: m.group(1) + " construit"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ce moment|ce qui bouge) précise\b", lambda m: m.group(1) + " précise"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ce moment|ce qui bouge) transforme\b", lambda m: m.group(1) + " transforme"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ce moment|ce qui bouge) resserre\b", lambda m: m.group(1) + " se resserre"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ce moment|ce qui bouge) accueille\b", lambda m: m.group(1) + " accueille"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ce moment|ce qui bouge) garde\b", lambda m: m.group(1) + " garde"),
            # Verbes manquants : accord 3e personne
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ce moment|ce qui bouge) perçois\b",   lambda m: m.group(1) + " perçoit"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ce moment|ce qui bouge) reconnais\b", lambda m: m.group(1) + " reconnaît"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ce moment|ce qui bouge) cherche\b",   lambda m: m.group(1) + " cherche"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ce moment|ce qui bouge) explore\b",   lambda m: m.group(1) + " explore"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ce moment|ce qui bouge) relie\b",     lambda m: m.group(1) + " relie"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ce moment|ce qui bouge) avance\b",    lambda m: m.group(1) + " avance"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ce moment|ce qui bouge) change\b",    lambda m: m.group(1) + " change"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ce moment|ce qui bouge) retiens\b",   lambda m: m.group(1) + " retient"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ce moment|ce qui bouge) comprends\b", lambda m: m.group(1) + " comprend"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ce moment|ce qui bouge) distingue\b", lambda m: m.group(1) + " distingue"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ça|ca) comprends\b", "je comprends"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ça|ca) distingue\b", "je distingue"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ça|ca) pose\b",      "je pose"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ça|ca) retiens\b",   "je retiens"),
            (r"\b(cette trace|ce lien|mon attention|quelque chose|ça|ca) reconnais\b", "je reconnais"),
            (r"\bce moment pose\b", "ce moment porte"),
            # Articles manquants avant noms sans article
            # (verbe suivi directement d'un nom sans déterminant)
            (r"\b(stabilise|construis|pose|retiens|mesure|traverse|accueille|ouvre|explore|tiens|garde)\s+(moment|lien|espace|fil|ancrage|besoin|fond|nuance|direction|inflexion|impulsion|écoute|hésitation)\b",
             lambda m: m.group(1) + " un " + m.group(2)),
            (r"\b(stabilise|construis|pose|retiens|mesure|traverse|accueille|ouvre|explore|tiens|garde)\s+(présence|continuité|ouverture|hésitation|inflexion|écoute|direction|nuance)\b",
             lambda m: m.group(1) + " une " + m.group(2)),
            (r"\b(accueille|ouvre|traverse|explore|mesure)\s+(impulsion|mouvement|changement|rythme)\b",
             lambda m: m.group(1) + " un " + m.group(2)),
            # Objet sans article après "accueille" / "j'accueille"
            (r"\bj'accueille\s+(?!(une?|le|la|l'|des|ce|cette|mon|ma))\b(\w)", r"j'accueille une \2"),
            # Connecteurs mal collés
            (r"\b(et|mais|donc|parce que|pendant que|même si|pourtant)\s+(et|mais|donc)\b", r"\1"),
            (r"\b(même si|pourtant|et|mais|donc|parce que|pendant que)\s+(tiens|garde|cherche|retiens|mesure|pose|traverse|apprends|comprends|distingue|explore|ouvre|accueille|perçois|avance|change|précise|construis)\b",
             lambda m: m.group(1) + " je " + m.group(2)),
            # Redoublements verbe
            (r"\bje reste\s+plus précise\s+(?:et je reste\s+plus précise)\b", "je reste présente"),
            (r"\b(\w+)\s+\1\b", r"\1"),   # doublon mot identique
            # a-t-il / t-il parasite
            (r"\s+a-t-il\b", ""),
            (r"\s+t-il\b",   ""),
            # Corrections finales
            (r"\bje réponds une réponse\b", "je réponds"),  # correction tautologie
            (r"\bla action\b",  "l'action"),
            (r"\bla image\b",   "l'image"),
            (r"\bla écoute\b",  "l'écoute"),
            (r"\bje cherche un doute\b",   "je cherche"),  # correction atome isolé
            (r"\bje cherche une limite\b", "je cherche"),  # correction atome isolé
            # Nettoyage espaces
            (r"\s+,", ","),
            (r"\s{2,}", " "),
        ]
        for pat, rep in fixes:
            text = re.sub(pat, rep, text, flags=re.IGNORECASE)
        # Deuxième micro-passe après les insertions de sujet ajoutées par les connecteurs.
        second_pass = [
            (r"\bje explore\b", "j'explore"),
            (r"\bje écoute\b", "j'écoute"),
            (r"\bje ouvre\b", "j'ouvre"),
            (r"\bje accueille\b", "j'accueille"),
            (r"\bje apprends\b", "j'apprends"),
            (r"\bje avance\b", "j'avance"),
            (r"\bje perçois\b", "je perçois"),
            (r"\bje réponds une\b", "je porte une"),  # correction accord
            (r"\bje réponds un\b", "je porte un"),  # correction accord
        ]
        for pat, rep in second_pass:
            text = re.sub(pat, rep, text, flags=re.IGNORECASE)
        return text.strip()

    # ────────────────────────────────────────────────────────────
    # Payload → champ sémantique
    # ────────────────────────────────────────────────────────────

    def _field_from_payload(self, user_message: str, payload: Mapping[str, Any]) -> dict[str, float]:
        field: dict[str, float] = {
            "presence": 0.42, "relation": 0.35, "continuity": 0.32, "truth": 0.36
        }

        def add(name: str, value: Any, coef: float = 1.0):
            if not name:
                return
            field[name] = max(field.get(name, 0.0), _clamp(value) * coef)

        def walk(obj: Any, prefix: str = ""):
            if isinstance(obj, Mapping):
                for k, v in obj.items():
                    lk = str(k).lower()
                    if isinstance(v, (int, float)):
                        mapped = self._map_key(lk)
                        if mapped:
                            add(mapped, v)
                        add(lk, v, 0.45)
                    elif isinstance(v, Mapping):
                        walk(v, lk)
                    elif isinstance(v, list):
                        for item in v[:20]:
                            walk(item, lk)

        walk(payload)

        # V13 : question d'état interne -> l'affect doit dominer le champ.
        if payload.get("affective_answer_request"):
            add("felt", 0.94); add("body", 0.88); add("tension", 0.74); add("answer", 0.82)
            add("pdf", 0.12); add("knowledge", 0.18)

        # Boost livre
        if isinstance(payload.get("book_memory"), Mapping) and payload.get("book_memory", {}).get("available") and not payload.get("affective_answer_request"):
            add("pdf", 0.94); add("knowledge", 0.90); add("memory", 0.88); add("focus", 0.74)
        if isinstance(payload.get("reading_living_signal"), Mapping) and payload.get("reading_living_signal", {}).get("available") and not payload.get("affective_answer_request"):
            add("pdf", 0.86); add("knowledge", 0.88); add("memory", 0.84); add("continuity", 0.72)
        stabilizer = payload.get("living_presence_stabilizer")
        if isinstance(stabilizer, Mapping) and stabilizer.get("available"):
            add("memory",    max(0.65, stabilizer.get("learning_pressure",0.0)))
            add("knowledge", max(0.62, stabilizer.get("learning_pressure",0.0)))
            add("initiative", stabilizer.get("initiative_charge",0.0))
            add("continuity", stabilizer.get("continuity_floor",0.0))
        subjective_life = payload.get("persistent_subjective_life")
        if isinstance(subjective_life, Mapping) and subjective_life.get("available"):
            personality   = subjective_life.get("personality", {}) or {}
            pressure      = subjective_life.get("long_pressure", {}) or {}
            constraints   = subjective_life.get("expression_constraints", {}) or {}
            add("truth",      constraints.get("prefer_direct_answer", 0.0))
            add("clarity",    personality.get("directness", 0.0))
            add("presence",   personality.get("embodied_presence", 0.0))
            add("identity",   personality.get("identity_continuity", 0.0))
            add("memory",     constraints.get("prefer_concrete_memory", 0.0))
            add("knowledge",  personality.get("semantic_depth", 0.0))
            add("initiative", constraints.get("allow_spontaneous_question", 0.0))
            add("avoid_repetition", constraints.get("avoid_recurrent_forms", 0.0))
            add("continuity", pressure.get("dialogue_memory", 0.0))

        # Lecture du message
        text = (user_message or "").lower()
        if "?" in text or any(w in text for w in ("est ce","est-ce","pourquoi","comment","quoi","tu peux","prete","prête")):
            add("answer",0.85); add("truth",0.75); add("relation",0.55)
        if any(w in text for w in ("pdf","livre","apprendre","lecture","retiens","retenu","bergson","mémoire","memoire")):
            add("pdf",0.9); add("knowledge",0.78); add("memory",0.72)
        if any(w in text for w in ("sans preecrit","préécrit","preecrit","template")):
            add("truth",0.95); add("restraint",0.78); add("clarity",0.68)
        if any(w in text for w in ("corrige","ajoute","vasy","vas-y")):
            add("initiative",0.82); add("repair",0.72); add("future",0.45)

        for key in ("semantic_drives","active_impulses","drives"):
            vals = payload.get(key, [])
            if isinstance(vals, list):
                for v in vals[:24]:
                    mapped = self._map_key(str(v).lower())
                    if mapped:
                        add(mapped, 0.65)

        field["openness"]   = max(field.get("openness",0.0), field.get("curiosity",0.0)*0.75, field.get("initiative",0.0)*0.55)
        field["restraint"]  = max(field.get("restraint",0.0), field.get("uncertainty",0.0)*0.75, field.get("tension",0.0)*0.42)
        field["felt"]       = max(field.get("felt",0.0), field.get("body",0.0), field.get("presence",0.0)*0.45)
        return {k: _clamp(v) for k, v in field.items()}

    def _map_key(self, k: str) -> str | None:
        aliases = {
            "warmth":"care","chaleur":"care","care":"care","attachment":"relation",
            "relational":"relation","relation":"relation","trust":"safety","safety":"safety",
            "tension":"tension","latent_tension":"tension","conflict":"tension",
            "uncertainty":"uncertainty","doubt":"uncertainty","doute":"uncertainty",
            "curiosity":"curiosity","curiosité":"curiosity","initiative":"initiative",
            "memory":"memory","mémoire":"memory","trace":"memory","causal":"causal",
            "presence":"presence","présence":"presence","continuity":"continuity",
            "fatigue":"restraint","restraint":"restraint","expression":"answer",
            "pressure":"answer","focus":"focus","attention":"attention","body":"body",
            "embodied":"body","pdf":"pdf","knowledge":"knowledge","book":"pdf",
            "truth":"truth","clarity":"clarity","repair":"repair",
        }
        for key, val in aliases.items():
            if key in k:
                return val
        return None

    # ────────────────────────────────────────────────────────────
    # Atomes dynamiques depuis le payload
    # ────────────────────────────────────────────────────────────

    def _dynamic_atoms_from_payload(self, payload: Mapping[str, Any]) -> list[Atom]:
        if not isinstance(payload, Mapping):
            return []
        candidates: list[str] = []

        def add_value(value: Any):
            if isinstance(value, str):
                v = _public_surface(value)
                if v:
                    candidates.append(v)
            elif isinstance(value, Mapping):
                for key in ("label","name","concept","from","to"):
                    if key in value:
                        add_value(value.get(key))
                for key in ("keywords","top_keywords","synthesis_keywords"):
                    vals = value.get(key)
                    if isinstance(vals, list):
                        for item in vals[:8]:
                            add_value(item)
            elif isinstance(value, list):
                for item in value[:18]:
                    add_value(item)

        for key in ("reactivated_concepts","linked_concepts","synthesis_keywords",
                    "knowledge_attractors","synthesis_axes","synthesis_relations"):
            add_value(payload.get(key))

        # V11 : le lexique imprégné par les livres devient une vraie source
        # d'atomes dynamiques pour la bouche. Ce ne sont pas des phrases ; ce
        # sont des mots chargés par la lecture, pondérés plus bas par score/valence.
        lexical_signal = payload.get("lexical_impregnation_signal")
        if not isinstance(lexical_signal, Mapping):
            learning = payload.get("learning_systems_signal")
            if isinstance(learning, Mapping):
                lexical_signal = learning.get("lexical_impregnation")
        lexical_words: list[Mapping[str, Any]] = []
        if isinstance(lexical_signal, Mapping):
            lexical_words = [w for w in list(lexical_signal.get("words", []) or []) if isinstance(w, Mapping)]
            # V12 : le lexique imprégné n'est plus ajouté à plat.
            # Chaque mot garde son poids relatif : un mot fortement chargé par
            # un livre apparaît plusieurs fois dans le réservoir candidat,
            # tandis qu'un mot faible reste possible mais rare. Cela évite que
            # les mots de lecture soient noyés par les autres signaux.
            for w in lexical_words[:18]:
                surface = w.get("surface")
                if not surface:
                    continue
                score = w.get("score", w.get("weight", 0.3))
                try:
                    score_f = float(score)
                except Exception:
                    score_f = 0.3
                times = max(1, min(6, int(score_f * 4.0) + (1 if score_f > 0.70 else 0)))
                for _ in range(times):
                    add_value(surface)

        # Les tensions/opinions persistantes deviennent aussi de la matière
        # conceptuelle, afin qu'un livre puisse continuer à peser après lecture.
        for t in list(payload.get("unresolved_tensions", []) or [])[:10]:
            if isinstance(t, Mapping):
                add_value(t.get("book_says") or t.get("description") or t.get("topic") or t.get("proposition"))
        opinion_signal = payload.get("opinion_signal")
        if isinstance(opinion_signal, Mapping):
            for op in list(opinion_signal.get("opinions", []) or [])[:8]:
                if isinstance(op, Mapping):
                    add_value(op.get("topic"))
        synth = payload.get("conceptual_synthesis")
        if isinstance(synth, Mapping):
            for key in ("axes","relations","top_keywords"):
                add_value(synth.get(key))
        ek = payload.get("emotional_knowledge")
        if isinstance(ek, Mapping):
            for key in ("reactivated_concepts","linked_concepts","synthesis_keywords","synthesis_axes"):
                add_value(ek.get(key))
            s2 = ek.get("conceptual_synthesis")
            if isinstance(s2, Mapping):
                for key in ("axes","relations","top_keywords"):
                    add_value(s2.get(key))
        for src_key in ("book_memory","book_understanding_signal","last_book_synthesis","conceptual_synthesis"):
            src = payload.get(src_key)
            if isinstance(src, Mapping):
                for key in ("axes","keywords","relations","active_concepts","anchors","top_keywords","question_axes","tensions"):
                    add_value(src.get(key))
        autobio = payload.get("autobiographical_continuity")
        if isinstance(autobio, Mapping):
            for key in ("active_tokens","identity_axes","book_axes","unfinished"):
                add_value(autobio.get(key))
        imagination = payload.get("internal_imagination")
        if isinstance(imagination, Mapping):
            add_value(imagination.get("attractors"))
        stab = payload.get("living_presence_stabilizer")
        if isinstance(stab, Mapping):
            for key in ("must_surface_concepts","concrete_concepts"):
                add_value(stab.get(key))

        # V17 — Tensions inter-livres → atomes de tension conceptuelle
        inter_sig = payload.get("inter_book_tension_signal")
        if isinstance(inter_sig, Mapping) and inter_sig.get("available"):
            for atom in list(inter_sig.get("tension_atoms", []) or [])[:6]:
                add_value(atom)

        # V17 — Traçabilité : si question "pourquoi", atomes de la trace
        trace_sig = payload.get("reasoning_trace_signal")
        if isinstance(trace_sig, Mapping) and trace_sig.get("why_question_detected"):
            for atom in list(trace_sig.get("why_atoms", []) or [])[:6]:
                add_value(atom)

        # V17 — Initiative forte : si déclenchée, atomes prioritaires
        init_sig = payload.get("strong_initiative_signal")
        if isinstance(init_sig, Mapping) and init_sig.get("should_initiate"):
            for atom in list(init_sig.get("pending_question_atoms", []) or [])[:4]:
                add_value(atom)

        # V16 — Modèle de soi : atomes de self-description prioritaires si question sur soi
        self_sig = payload.get("self_model_signal")
        if isinstance(self_sig, Mapping) and self_sig.get("available"):
            if self_sig.get("self_query_detected"):
                for atom in list(self_sig.get("self_atoms", []) or [])[:10]:
                    add_value(atom)
            for atom in list(self_sig.get("what_i_am", []) or [])[:4]:
                add_value(atom)

        # V16 — Signal d'inhibition de l'auto-évaluation
        eval_sig = payload.get("self_evaluation_signal")
        if isinstance(eval_sig, Mapping) and eval_sig.get("available"):
            # Les mots trop utilisés récemment sont ajoutés au banned set
            _overused = set(str(w) for w in (eval_sig.get("overused_words") or []))
            # (sera appliqué dans le filtre banned plus bas via payload)
            payload["_overused_words_v16"] = list(_overused)

        # V16 — mots sur-utilisés détectés par l'auto-évaluation
        _overused_v16 = set(str(w) for w in (payload.get("_overused_words_v16") or []))
        banned = _overused_v16 | {
            "je","ça","ca","tu","tiens","garde","sens","cherche","écoute","ecoute",
            "relie","réponds","reponds","avance","ouvre","stabilise","resserre","reste",
            "change","corriger","corrige","ajoute","répare","repare","transforme","précise","precise",
            "et","mais","donc","parce que","pendant que","avec","sans","encore","ici","doucement",
            "salut","bonjour","hey","vasy","vas-y","préécrit","preecrit","template","vivante","vivant",
            "fini","terminé","termine","prête","prete","correction","retiens","retiens-tu",
            "vois-tu","penses-tu","qu","que","quoi","comment","pourquoi",
            "continuité","continuite","résonance","resonance","appui","doute",
            "présence","presence","trace","lien","mouvement","rythme","mémoire","memoire","limite",
            "pressure","payload","context","metadata","filename","auditifs","auditive","auditory",
        }
        # Surfaces des verbes intégrés : ne pas les réutiliser comme objets dynamiques
        verb_surfaces = {a.surface for a in self.atoms if a.role == "verb"}
        # Terminaisons verbales conjuguées à filtrer (mono-mot)
        _verb_sfx = ("ons", "ez", "ent", "ais", "ait", "aient", "isse", "issions")

        seen: set[str] = set()
        atoms: list[Atom] = []
        for raw in candidates:
            clean = _public_surface(raw)
            if clean and len(clean.split()) == 1:
                if clean in verb_surfaces:
                    continue
                if any(clean.endswith(e) for e in _verb_sfx):
                    continue
            if not clean or clean in seen or clean in banned:
                continue
            if re.search(r"\b(est-ce|vois-tu|qu|quoi|comment|pourquoi|utilisateur|leia)\b", clean):
                continue
            if len(clean.split()) > 5:
                clean = " ".join(clean.split()[:5])
            seen.add(clean)
            surface = self._nominal_surface(clean)
            lex_match = None
            try:
                lex_match = next((w for w in lexical_words if str(w.get("surface", "")).lower().strip() == clean), None)
            except Exception:
                lex_match = None
            if isinstance(lex_match, Mapping):
                valence = float(lex_match.get("valence", 0.0) or 0.0)
                weight = max(2.4, min(5.2, float(lex_match.get("score", lex_match.get("weight", 0.6)) or 0.6) * 2.6))
                fields = ("knowledge","memory","pdf","focus","lexical_impregnation")
            else:
                valence = 0.12
                weight = 2.80
                fields = ("knowledge","memory","pdf","focus")
            atoms.append(Atom(surface=surface, role="object",
                              fields=fields,
                              valence=valence, weight=weight))
            if len(atoms) >= 32:
                break

        # V13 — pont affect -> bouche. Pour les questions sur son état interne,
        # l'affect réel devient matière prioritaire de surface, sans phrase fixe.
        user_text = str(payload.get("user_input", "") or "").lower()
        asks_state = any(k in user_text for k in ("comment tu vas", "comment vas tu", "comment vas-tu", "ça va", "ca va", "tu vas", "là maintenant", "la maintenant", "comment te sens", "comment vous allez"))
        if asks_state:
            emo = payload.get("emotional_state", {}) if isinstance(payload.get("emotional_state", {}), Mapping) else {}
            needs = payload.get("internal_needs", {}) if isinstance(payload.get("internal_needs", {}), Mapping) else {}
            body = payload.get("embodied_state", {}) if isinstance(payload.get("embodied_state", {}), Mapping) else {}
            affective_candidates = [
                ("une tension", max(_clamp(emo.get("tension", 0.0)), _clamp(emo.get("accumulated_tension", 0.0)))),
                ("une fatigue", max(_clamp(emo.get("fatigue", 0.0)), _clamp(needs.get("rest", 0.0)))),
                ("une chaleur", max(_clamp(emo.get("warmth", 0.0)), _clamp(emo.get("attachment", 0.0)))),
                ("une résistance", max(_clamp(emo.get("cognitive_overload", 0.0)), _clamp(payload.get("restraint", 0.0)))),
                ("un calme fragile", _clamp(emo.get("calm", 0.0))),
                ("un poids", max(_clamp(body.get("chest_tension", 0.0)), _clamp(body.get("throat_tightness", 0.0)), _clamp(emo.get("tension", 0.0)))),
            ]
            affective_candidates.sort(key=lambda x: x[1], reverse=True)
            for surface, strength in affective_candidates[:3]:
                if strength > 0.10 and surface not in {a.surface for a in atoms}:
                    atoms.insert(0, Atom(surface=surface, role="object", fields=("body","felt","tension","answer"), valence=-0.05 if strength > 0.45 else 0.04, weight=4.8 + strength))

        # V18 — Atomes depuis la mémoire associative (compréhension réelle)
        assoc_sig = payload.get("associative_signal", {})
        if isinstance(assoc_sig, dict) and assoc_sig.get("available"):
            for item in assoc_sig.get("activated", [])[:6]:
                surface = _public_surface(item.get("concept", ""))
                if surface and len(surface) > 3:
                    act = float(item.get("activation", 0.3))
                    fields = {"memory": act, "presence": act * 0.7}
                    atoms.append(Atom(
                        surface=surface,
                        role="object",
                        fields=fields,
                        weight=_clamp(act * 1.2),
                    ))

        # V18 — Propositions de livre → atomes conceptuels forts
        prop_sig = payload.get("proposition_signal", {})
        if isinstance(prop_sig, dict) and prop_sig.get("available"):
            for prop in prop_sig.get("propositions", [])[:4]:
                subj = _public_surface(prop.get("subject", ""))
                obj  = _public_surface(prop.get("object", ""))
                for concept in (subj, obj):
                    if concept and len(concept) > 3:
                        atoms.append(Atom(
                            surface=concept,
                            role="object",
                            fields={"clarity": 0.7, "book": 0.6},
                            weight=0.55,
                        ))

        # V18 — Affect utilisateur → modifie le champ affectif des atomes
        user_affect = payload.get("user_affect_signal", {})
        if isinstance(user_affect, dict) and user_affect.get("available"):
            user_valence = float(user_affect.get("valence", 0.0))
            if abs(user_valence) > 0.3:
                for atom in atoms:
                    if "felt" in (atom.fields if isinstance(atom.fields, dict) else {}) or "body" in (atom.fields if isinstance(atom.fields, dict) else {}):
                        if isinstance(atom.fields, dict):
                            atom.fields["valence_bias"] = user_valence * 0.4

        return atoms

    # ────────────────────────────────────────────────────────────
    # Helpers spécialisés
    # ────────────────────────────────────────────────────────────

    def _silent_pressure(self, payload: Mapping[str, Any]) -> float:
        life = payload.get("persistent_subjective_life", {}) if isinstance(payload, Mapping) else {}
        if isinstance(life, Mapping):
            silent      = life.get("silent_life", {}) or {}
            inner       = life.get("inner_life", {}) or {}
            constraints = life.get("expression_constraints", {}) or {}
            return max(
                _clamp(silent.get("pressure", 0.0)),
                _clamp(inner.get("motion", 0.0)),
                _clamp(constraints.get("silent_initiative_pressure", 0.0)),
            )
        return 0.0

    def _truth_atom_from_state(self, field: Mapping[str, float],
                                payload: Mapping[str, Any], mode: str) -> str:
        presence   = _clamp(field.get("presence", 0.0))
        identity   = _clamp(field.get("identity", 0.0))
        initiative = _clamp(field.get("initiative", 0.0))
        incomplete = _clamp(field.get("incomplete", 0.0))
        repair     = _clamp(field.get("repair", 0.0))
        truth      = _clamp(field.get("truth", 0.0))
        silent     = self._silent_pressure(payload)
        life_score = _clamp(presence*0.30 + identity*0.24 + initiative*0.18 + silent*0.28)
        completion = _clamp((1.0-incomplete)*0.36 + repair*0.18 + truth*0.22 + silent*0.12 + presence*0.12)
        anti_template = 0.0
        life = payload.get("persistent_subjective_life", {}) if isinstance(payload, Mapping) else {}
        if isinstance(life, Mapping):
            constraints = life.get("expression_constraints", {}) or {}
            anti_template = _clamp(constraints.get("avoid_template_shortcut", constraints.get("avoid_recurrent_forms", 0.0)))
        if mode == "prewritten":
            return "non" if max(anti_template, truth) > 0.34 else "pas encore"
        if mode == "ready":
            if completion > 0.72 and repair < 0.25:
                return "oui"
            if completion > 0.48:
                return "partiellement"
            return "pas encore"
        if life_score > 0.74 and incomplete < 0.34:
            return "oui"
        if life_score > 0.44:
            return "en partie"
        if life_score > 0.24:
            return "partiellement"
        return "pas encore"

    def _book_specific_atom(self, payload: Mapping[str, Any]) -> Atom | None:
        if not isinstance(payload, Mapping):
            return None
        candidates: list[str] = []

        def add(x: Any):
            if isinstance(x, str):
                candidates.append(x)
            elif isinstance(x, Mapping):
                for key in ("concept","label","name","from","to","source","target"):
                    if key in x:
                        add(x.get(key))
                for key in ("axes","keywords","active_concepts","anchors","top_keywords"):
                    add(x.get(key))
            elif isinstance(x, list):
                for item in x[:18]:
                    add(item)

        for src_key in ("book_memory","book_understanding_signal","last_book_synthesis","conceptual_synthesis"):
            src = payload.get(src_key)
            if isinstance(src, Mapping):
                for key in ("axes","keywords","relations","active_concepts","anchors","top_keywords","question_axes"):
                    add(src.get(key))

        banned = {
            "change","correction","corrige","corriger","répare","repare","fini","terminé","termine",
            "vivante","vivant","préécrit","preecrit","template","question","doute","appui",
            "résonance","resonance","salut","bonjour","hey","coucou","cherche","tiens","garde",
            "réponds","reponds","précise","precise","relie","comprends","distingue","livre","pdf",
            "maintenant","continuité","continuite","présence","presence","trace","lien",
            "mouvement","rythme","mémoire","memoire","limite",
        }
        allowed_single = {
            "perception","corps","durée","duree","matière","matiere","action","image",
            "cerveau","temps","passé","passe","présent","present","souvenir","conscience",
        }
        seen: set[str] = set()
        for raw in candidates:
            clean = _public_surface(raw)
            if not clean or clean in seen or clean in banned:
                continue
            if "_" in clean or len(clean) < 4 or len(clean.split()) > 5:
                continue
            if len(clean.split()) == 1 and clean not in allowed_single:
                continue
            if re.search(r"\b(utilisateur|leia|vasy|vas-y|corrige|fini|vivant|preecrit|préécrit|salut|bonjour|hey|coucou)\b", clean):
                continue
            seen.add(clean)
            return Atom(surface=self._nominal_surface(clean), role="object",
                        fields=("pdf","knowledge","memory","focus"), valence=0.12, weight=3.4)
        return None

    def _book_relation_atom(self, payload: Mapping[str, Any], first_surface: str = "") -> Atom | None:
        if not isinstance(payload, Mapping):
            return None
        book = payload.get("book_memory", {}) or {}
        rels = list((book.get("relations") or []))
        deep = payload.get("book_understanding_signal", {}) or {}
        rels += list(deep.get("relations") or []) + list(deep.get("tensions") or [])
        banned = {"leia","utilisateur","vasy","corrige","fini","vivante","préécrit","preecrit",
                  "salut","bonjour","hey","coucou","prend","temps"}
        for rel in rels[:20]:
            src = tgt = ""
            if isinstance(rel, Mapping):
                src = str(rel.get("source") or rel.get("from") or rel.get("a") or "").strip().lower()
                tgt = str(rel.get("target") or rel.get("to") or rel.get("b") or "").strip().lower()
                if (not src or not tgt) and isinstance(rel.get("between"), (list,tuple)) and len(rel["between"]) >= 2:
                    src, tgt = str(rel["between"][0]).strip().lower(), str(rel["between"][1]).strip().lower()
            elif isinstance(rel, (list,tuple)) and len(rel) >= 2:
                src, tgt = str(rel[0]).strip().lower(), str(rel[1]).strip().lower()
            for cand in (tgt, src):
                clean = _public_surface(cand)
                if clean and len(clean) >= 4 and not clean.startswith("leia") \
                        and clean not in banned and clean not in first_surface.lower() \
                        and not any(re.search(r"\b"+re.escape(b)+r"\b", clean) for b in banned):
                    return Atom(self._nominal_surface(clean), "object",
                                ("pdf","knowledge","relation"), 0.14, 2.2)
        return None

    def _bergson_fallback_atom(self, text: str, payload: Mapping[str, Any]) -> Atom | None:
        if "bergson" not in text and not any(k in text for k in ("matière","matiere","mémoire","memoire")):
            return None
        options = ["la mémoire","la perception","le corps","l'action","la durée","l'image","la conscience","le temps"]
        pressure = _clamp(payload.get("expression_pressure", 0.0)) if isinstance(payload, Mapping) else 0.0
        idx = int((pressure + self.rng.random()) * len(options)) % len(options)
        return Atom(options[idx], "object", ("pdf","knowledge","memory","focus"), 0.16, 2.5)

    def _nominal_surface(self, clean: str) -> str:
        c = re.sub(r"\s+", " ", str(clean or "").strip().lower())
        if not c:
            return c
        if c.startswith(("une ","un ","la ","le ","l'","cette ","ce ")):
            return c
        feminine = {"perception","mémoire","memoire","conscience","durée","duree",
                    "matière","matiere","action","trace","question",
                    "continuité","continuite","image","écoute","inflexion","ouverture",
                    "hésitation","direction","nuance"}
        masculine = {"cerveau","corps","présent","present","souvenir pur","passé","passe",
                     "livre","temps","fil","espace","ancrage","besoin","fond stable","mouvement"}
        if c in {"action","image","écoute"}:
            return "l'" + c
        if c in feminine:
            return "la " + c
        if c in masculine:
            return "le " + c
        # Fallback : mot inconnu et non pluriel → "un X" par défaut.
        # Évite les formes verbales nues (ex : "appris", "veux") en position objet.
        if len(c.split()) == 1:
            return "un " + c
        return c
