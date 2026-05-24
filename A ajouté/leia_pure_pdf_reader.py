# leia_pure_pdf_reader.py
# Project Leia / project_leia — V19+
#
# Lecteur PDF pur Python, ZÉRO dépendance externe.
# Utilise uniquement la bibliothèque standard : re, zlib, struct, io, time,
# pathlib, dataclasses, collections.
#
# Ce module remplace/complète pdf_knowledge_engine.py en supprimant
# la dépendance à pypdf/PyPDF2. Il parse le format PDF binaire en natif,
# extrait le texte réel avec encodages et CMap ToUnicode, puis envoie
# chaque fragment dans le pipeline de compréhension vivante de Leia.
#
# Architecture interne :
#   PDFParseError        — exception propre
#   PDFLexer             — tokeniseur du langage PDF
#   PDFParser            — parse les objets PDF depuis les tokens
#   PDFDocument          — xref, objets indirects, chiffrement détecté
#   PDFFont              — décodage d'encodages (WinAnsi, MacRoman, ToUnicode CMap)
#   PDFContentParser     — extrait le texte depuis les flux de contenu
#   LeiaPurePDFReader    — interface principale, compatible avec LeiaPDFKnowledgeEngine

from __future__ import annotations

import io
import json
import math
import re
import struct
import time
import zlib
from collections import defaultdict
from dataclasses import asdict, dataclass, field, is_dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Generator, Iterable, List, Mapping, Optional, Tuple, Union


# ---------------------------------------------------------------------------
# Constantes & outils
# ---------------------------------------------------------------------------

ProgressCallback = Callable[[str], None]

# Encodage WinAnsiEncoding (cp1252) — table caractères 128-255
_WINANSI: Dict[int, str] = {
    0x80: "\u20AC", 0x82: "\u201A", 0x83: "\u0192", 0x84: "\u201E",
    0x85: "\u2026", 0x86: "\u2020", 0x87: "\u2021", 0x88: "\u02C6",
    0x89: "\u2030", 0x8A: "\u0160", 0x8B: "\u2039", 0x8C: "\u0152",
    0x8E: "\u017D", 0x91: "\u2018", 0x92: "\u2019", 0x93: "\u201C",
    0x94: "\u201D", 0x95: "\u2022", 0x96: "\u2013", 0x97: "\u2014",
    0x98: "\u02DC", 0x99: "\u2122", 0x9A: "\u0161", 0x9B: "\u203A",
    0x9C: "\u0153", 0x9E: "\u017E", 0x9F: "\u0178",
}
# Rempli par Latin-1 au-dessous de 128 et au-dessus de 0x9F
for _i in range(0x20, 0x80):
    _WINANSI[_i] = chr(_i)
for _i in range(0xA0, 0x100):
    _WINANSI[_i] = chr(_i)

# Glyphes PDF standard → Unicode (extrait des noms de glyphes Adobe)
_GLYPH_TO_UNICODE: Dict[str, str] = {
    "space": " ", "exclam": "!", "quotedbl": '"', "numbersign": "#",
    "dollar": "$", "percent": "%", "ampersand": "&", "quotesingle": "'",
    "parenleft": "(", "parenright": ")", "asterisk": "*", "plus": "+",
    "comma": ",", "hyphen": "-", "period": ".", "slash": "/",
    "colon": ":", "semicolon": ";", "less": "<", "equal": "=",
    "greater": ">", "question": "?", "at": "@", "bracketleft": "[",
    "backslash": "\\", "bracketright": "]", "asciicircum": "^",
    "underscore": "_", "grave": "`", "braceleft": "{", "bar": "|",
    "braceright": "}", "asciitilde": "~",
    "quotedblleft": "\u201C", "quotedblright": "\u201D",
    "quoteleft": "\u2018", "quoteright": "\u2019",
    "endash": "\u2013", "emdash": "\u2014",
    "bullet": "\u2022", "ellipsis": "\u2026",
    "fi": "fi", "fl": "fl", "ff": "ff", "ffi": "ffi", "ffl": "ffl",
    "Euro": "\u20AC", "trademark": "\u2122", "copyright": "\u00A9",
    "registered": "\u00AE",
    "Agrave": "\u00C0", "Aacute": "\u00C1", "Acircumflex": "\u00C2",
    "Atilde": "\u00C3", "Adieresis": "\u00C4", "Aring": "\u00C5",
    "AE": "\u00C6", "Ccedilla": "\u00C7", "Egrave": "\u00C8",
    "Eacute": "\u00C9", "Ecircumflex": "\u00CA", "Edieresis": "\u00CB",
    "Igrave": "\u00CC", "Iacute": "\u00CD", "Icircumflex": "\u00CE",
    "Idieresis": "\u00CF", "Eth": "\u00D0", "Ntilde": "\u00D1",
    "Ograve": "\u00D2", "Oacute": "\u00D3", "Ocircumflex": "\u00D4",
    "Otilde": "\u00D5", "Odieresis": "\u00D6", "Oslash": "\u00D8",
    "Ugrave": "\u00D9", "Uacute": "\u00DA", "Ucircumflex": "\u00DB",
    "Udieresis": "\u00DC", "Yacute": "\u00DD", "Thorn": "\u00DE",
    "germandbls": "\u00DF", "agrave": "\u00E0", "aacute": "\u00E1",
    "acircumflex": "\u00E2", "atilde": "\u00E3", "adieresis": "\u00E4",
    "aring": "\u00E5", "ae": "\u00E6", "ccedilla": "\u00E7",
    "egrave": "\u00E8", "eacute": "\u00E9", "ecircumflex": "\u00EA",
    "edieresis": "\u00EB", "igrave": "\u00EC", "iacute": "\u00ED",
    "icircumflex": "\u00EE", "idieresis": "\u00EF", "eth": "\u00F0",
    "ntilde": "\u00F1", "ograve": "\u00F2", "oacute": "\u00F3",
    "ocircumflex": "\u00F4", "otilde": "\u00F5", "odieresis": "\u00F6",
    "oslash": "\u00F8", "ugrave": "\u00F9", "uacute": "\u00FA",
    "ucircumflex": "\u00FB", "udieresis": "\u00FC", "yacute": "\u00FD",
    "thorn": "\u00FE", "ydieresis": "\u00FF",
}
# Génère a-z, A-Z, 0-9 automatiquement
for _c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
    _GLYPH_TO_UNICODE[_c] = _c


def _clamp(v: Any, lo: float = 0.0, hi: float = 1.0) -> float:
    try:
        f = float(v)
        if math.isnan(f) or math.isinf(f):
            return lo
        return max(lo, min(hi, f))
    except Exception:
        return lo


def _jsonable(value: Any, depth: int = 0) -> Any:
    if depth > 6:
        return str(value)[:400]
    if is_dataclass(value):
        try:
            return _jsonable(asdict(value), depth + 1)
        except Exception:
            return str(value)[:400]
    if isinstance(value, Mapping):
        return {str(k): _jsonable(v, depth + 1) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_jsonable(v, depth + 1) for v in list(value)[:80]]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)[:400]


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------

class PDFParseError(Exception):
    pass


# ---------------------------------------------------------------------------
# Décodage des flux (filtres PDF)
# ---------------------------------------------------------------------------

def _decode_stream(data: bytes, filters: Any, decode_parms: Any = None) -> bytes:
    """Applique les filtres PDF à des données brutes de flux."""
    if filters is None:
        return data
    if isinstance(filters, str):
        filters = [filters]
    if not isinstance(filters, list):
        filters = [str(filters)]
    if decode_parms is None:
        decode_parms = [{}] * len(filters)
    elif isinstance(decode_parms, Mapping):
        decode_parms = [decode_parms] + [{}] * (len(filters) - 1)
    elif not isinstance(decode_parms, list):
        decode_parms = [{}] * len(filters)
    while len(decode_parms) < len(filters):
        decode_parms.append({})

    buf = data
    for filt, parms in zip(filters, decode_parms):
        filt = str(filt).strip("/").lower()
        parms = parms if isinstance(parms, Mapping) else {}
        if filt in ("flatedecode", "fl"):
            try:
                buf = zlib.decompress(buf)
            except zlib.error:
                try:
                    buf = zlib.decompress(buf, -15)  # raw deflate sans header
                except zlib.error:
                    pass  # retourne ce qu'on a
        elif filt in ("asciihexdecode", "ahx"):
            buf = bytes.fromhex(
                re.sub(rb"\s+", b"", buf).rstrip(b">").decode("ascii", errors="ignore")
            )
        elif filt in ("ascii85decode", "a85"):
            buf = _decode_ascii85(buf)
        elif filt in ("lzwdecode", "lzw"):
            buf = _decode_lzw(buf, parms)
        # RunLengthDecode, CCITTFaxDecode, JBIG2Decode : on laisse passer
    return buf


def _decode_ascii85(data: bytes) -> bytes:
    """Décode le filtre ASCII85."""
    data = data.rstrip(b"~>").replace(b"\n", b"").replace(b"\r", b"").replace(b" ", b"")
    out = bytearray()
    i = 0
    while i < len(data):
        if data[i:i+1] == b"z":
            out += b"\x00\x00\x00\x00"
            i += 1
        else:
            group = data[i:i+5]
            i += 5
            if len(group) < 5:
                padding = 5 - len(group)
                group = group + b"u" * padding
            else:
                padding = 0
            v = 0
            for byte in group:
                v = v * 85 + (byte - 33)
            result = struct.pack(">I", v)
            out += result[:4 - padding]
    return bytes(out)


def _decode_lzw(data: bytes, parms: Mapping) -> bytes:
    """Décode LZW minimal (Early Change = 1 par défaut)."""
    early = int((parms or {}).get("EarlyChange", 1))
    table: List[bytes] = [bytes([i]) for i in range(256)] + [b"", b""]
    result = bytearray()
    buf = int.from_bytes(data, "big")
    total_bits = len(data) * 8
    pos = 0
    code_size = 9
    prev: Optional[bytes] = None

    def read_code() -> Optional[int]:
        nonlocal pos, code_size
        if pos + code_size > total_bits:
            return None
        shift = total_bits - pos - code_size
        code = (buf >> shift) & ((1 << code_size) - 1)
        pos += code_size
        return code

    while True:
        code = read_code()
        if code is None:
            break
        if code == 256:  # Clear
            table = [bytes([i]) for i in range(256)] + [b"", b""]
            code_size = 9
            prev = None
            continue
        if code == 257:  # EOD
            break
        if code < len(table):
            entry = table[code]
        elif prev is not None:
            entry = prev + prev[:1]
        else:
            break
        result += entry
        if prev is not None:
            table.append(prev + entry[:1])
        prev = entry
        # Ajuste la taille de code
        next_threshold = (1 << code_size) - (1 if early else 0)
        if len(table) >= next_threshold and code_size < 12:
            code_size += 1
    return bytes(result)


# ---------------------------------------------------------------------------
# Tokeniseur PDF
# ---------------------------------------------------------------------------

class PDFLexer:
    """Tokeniseur bas niveau pour le langage PDF."""

    _WHITESPACE = b"\x00\t\n\x0C\r "
    _DELIMITERS = b"()<>[]{}/%"

    def __init__(self, data: bytes, offset: int = 0) -> None:
        self._data = data
        self._pos = offset
        self._len = len(data)

    @property
    def pos(self) -> int:
        return self._pos

    @pos.setter
    def pos(self, v: int) -> None:
        self._pos = max(0, min(v, self._len))

    def peek(self) -> Optional[int]:
        if self._pos < self._len:
            return self._data[self._pos]
        return None

    def skip_whitespace_and_comments(self) -> None:
        d = self._data
        n = self._len
        while self._pos < n:
            b = d[self._pos]
            if b in (0x00, 0x09, 0x0A, 0x0C, 0x0D, 0x20):
                self._pos += 1
            elif b == 0x25:  # '%' — commentaire jusqu'à EOL
                while self._pos < n and d[self._pos] not in (0x0A, 0x0D):
                    self._pos += 1
            else:
                break

    def read_token(self) -> Optional[bytes]:
        self.skip_whitespace_and_comments()
        if self._pos >= self._len:
            return None
        b = self._data[self._pos]
        # Chaîne littérale
        if b == 0x28:  # '('
            return self._read_literal_string()
        # Chaîne hexadécimale ou dictionnaire '<<'
        if b == 0x3C:  # '<'
            if self._pos + 1 < self._len and self._data[self._pos + 1] == 0x3C:
                self._pos += 2
                return b"<<"
            return self._read_hex_string()
        if b == 0x3E:  # '>'
            if self._pos + 1 < self._len and self._data[self._pos + 1] == 0x3E:
                self._pos += 2
                return b">>"
            self._pos += 1
            return b">"
        # Délimiteurs simples
        if b in (0x5B, 0x5D, 0x7B, 0x7D):  # [ ] { }
            self._pos += 1
            return bytes([b])
        # Nom
        if b == 0x2F:  # '/'
            return self._read_name()
        # Mot clé ou nombre
        return self._read_regular_token()

    def _read_literal_string(self) -> bytes:
        """Lit une chaîne PDF (...)  avec gestion des parenthèses imbriquées."""
        assert self._data[self._pos] == 0x28
        self._pos += 1
        out = bytearray()
        depth = 1
        d = self._data
        n = self._len
        while self._pos < n and depth > 0:
            b = d[self._pos]
            if b == 0x5C:  # backslash
                self._pos += 1
                if self._pos >= n:
                    break
                esc = d[self._pos]
                self._pos += 1
                if esc == 0x6E:
                    out.append(0x0A)
                elif esc == 0x72:
                    out.append(0x0D)
                elif esc == 0x74:
                    out.append(0x09)
                elif esc == 0x62:
                    out.append(0x08)
                elif esc == 0x66:
                    out.append(0x0C)
                elif esc == 0x28:
                    out.append(0x28)
                elif esc == 0x29:
                    out.append(0x29)
                elif esc == 0x5C:
                    out.append(0x5C)
                elif 0x30 <= esc <= 0x37:  # octal
                    octal = bytes([esc])
                    for _ in range(2):
                        if self._pos < n and 0x30 <= d[self._pos] <= 0x37:
                            octal += bytes([d[self._pos]])
                            self._pos += 1
                    out.append(int(octal, 8))
                elif esc in (0x0A, 0x0D):
                    if esc == 0x0D and self._pos < n and d[self._pos] == 0x0A:
                        self._pos += 1
                else:
                    out.append(esc)
            elif b == 0x28:
                depth += 1
                out.append(b)
                self._pos += 1
            elif b == 0x29:
                depth -= 1
                if depth > 0:
                    out.append(b)
                self._pos += 1
            else:
                out.append(b)
                self._pos += 1
        return b"(" + bytes(out) + b")"

    def _read_hex_string(self) -> bytes:
        """Lit une chaîne hex < ... >"""
        assert self._data[self._pos] == 0x3C
        self._pos += 1
        start = self._pos
        d = self._data
        n = self._len
        while self._pos < n and d[self._pos] != 0x3E:
            self._pos += 1
        content = d[start:self._pos]
        if self._pos < n:
            self._pos += 1  # skip '>'
        return b"<" + content + b">"

    def _read_name(self) -> bytes:
        """Lit un nom PDF /..."""
        assert self._data[self._pos] == 0x2F
        self._pos += 1
        d = self._data
        n = self._len
        start = self._pos
        while self._pos < n:
            b = d[self._pos]
            if b in self._WHITESPACE or b in self._DELIMITERS:
                break
            self._pos += 1
        return b"/" + d[start:self._pos]

    def _read_regular_token(self) -> bytes:
        d = self._data
        n = self._len
        start = self._pos
        while self._pos < n:
            b = d[self._pos]
            if b in self._WHITESPACE or b in self._DELIMITERS:
                break
            self._pos += 1
        return d[start:self._pos]

    def read_line(self) -> bytes:
        d = self._data
        n = self._len
        start = self._pos
        while self._pos < n and d[self._pos] not in (0x0A, 0x0D):
            self._pos += 1
        result = d[start:self._pos]
        if self._pos < n and d[self._pos] == 0x0D:
            self._pos += 1
        if self._pos < n and d[self._pos] == 0x0A:
            self._pos += 1
        return result


# ---------------------------------------------------------------------------
# Parseur d'objets PDF
# ---------------------------------------------------------------------------

class PDFParser:
    """Parse les objets PDF depuis un PDFLexer."""

    def __init__(self, lexer: PDFLexer) -> None:
        self._lex = lexer

    def parse_object(self) -> Any:
        """Parse le prochain objet PDF complet."""
        tok = self._lex.read_token()
        if tok is None:
            return None
        return self._parse_token(tok)

    def _parse_token(self, tok: bytes) -> Any:
        if tok == b"null":
            return None
        if tok == b"true":
            return True
        if tok == b"false":
            return False
        if tok == b"[":
            return self._parse_array()
        if tok == b"<<":
            return self._parse_dict()
        if tok and tok[0:1] == b"/":
            return tok[1:].decode("latin-1")  # nom PDF
        if tok and tok[0:1] in (b"(", b"<"):
            return self._decode_string(tok)
        # Essai de nombre
        try:
            if b"." in tok:
                return float(tok)
            v = int(tok)
            # Potentiellement "num gen R" — référence indirecte
            saved = self._lex.pos
            tok2 = self._lex.read_token()
            if tok2 is not None and tok2.isdigit():
                tok3 = self._lex.read_token()
                if tok3 == b"R":
                    return ("ref", v, int(tok2))
                # Remonte
                self._lex.pos = saved + len(tok2) + 1
            else:
                self._lex.pos = saved
            return v
        except (ValueError, TypeError):
            return tok.decode("latin-1", errors="replace")

    def _parse_array(self) -> List[Any]:
        result = []
        while True:
            self._lex.skip_whitespace_and_comments()
            tok = self._lex.read_token()
            if tok is None or tok == b"]":
                break
            result.append(self._parse_token(tok))
        return result

    def _parse_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        while True:
            self._lex.skip_whitespace_and_comments()
            tok = self._lex.read_token()
            if tok is None or tok == b">>":
                break
            if tok and tok[0:1] == b"/":
                key = tok[1:].decode("latin-1")
                value = self.parse_object()
                result[key] = value
        return result

    @staticmethod
    def _decode_string(tok: bytes) -> bytes:
        """Décode une chaîne PDF (littérale ou hex) en bytes bruts."""
        if tok.startswith(b"<") and tok.endswith(b">"):
            hex_content = tok[1:-1].replace(b" ", b"").replace(b"\n", b"").replace(b"\r", b"")
            if len(hex_content) % 2 != 0:
                hex_content += b"0"
            try:
                return bytes.fromhex(hex_content.decode("ascii", errors="ignore"))
            except Exception:
                return b""
        if tok.startswith(b"(") and tok.endswith(b")"):
            return tok[1:-1]
        return tok


# ---------------------------------------------------------------------------
# Document PDF — xref + résolution d'objets
# ---------------------------------------------------------------------------

class PDFDocument:
    """Représente un document PDF chargé en mémoire."""

    def __init__(self, data: bytes) -> None:
        self._data = data
        self._xref: Dict[int, int] = {}          # num → offset
        self._xref_gen: Dict[int, int] = {}       # num → génération
        self._obj_stream_cache: Dict[int, Dict[int, Any]] = {}  # stream_num → {obj_num: obj}
        self.trailer: Dict[str, Any] = {}
        self.encrypted = False
        self._parse()

    # ------------------------------------------------------------------
    # Parsing initial
    # ------------------------------------------------------------------

    def _parse(self) -> None:
        data = self._data
        # Cherche "startxref" en partant de la fin
        tail = data[-1024:] if len(data) > 1024 else data
        m = list(re.finditer(rb"startxref\s+(\d+)", tail))
        if not m:
            raise PDFParseError("startxref introuvable")
        xref_offset = int(m[-1].group(1))
        self._load_xref_chain(xref_offset)
        if "Encrypt" in self.trailer:
            self.encrypted = True

    def _load_xref_chain(self, offset: int) -> None:
        """Charge toute la chaîne xref (Prev inclus)."""
        visited: set = set()
        while offset is not None and offset not in visited:
            visited.add(offset)
            self._load_xref_at(offset)
            prev = self.trailer.get("Prev")
            if prev and isinstance(prev, (int, float)):
                offset = int(prev)
            else:
                break

    def _load_xref_at(self, offset: int) -> None:
        data = self._data
        # Detecte xref table classique ou xref stream
        chunk = data[offset:offset+10].lstrip(b"\r\n\t ")
        if chunk.startswith(b"xref"):
            self._parse_xref_table(offset)
        else:
            self._parse_xref_stream(offset)

    def _parse_xref_table(self, offset: int) -> None:
        lex = PDFLexer(self._data, offset)
        tok = lex.read_token()  # 'xref'
        if tok != b"xref":
            return
        while True:
            lex.skip_whitespace_and_comments()
            tok = lex.read_token()
            if tok is None or tok == b"trailer":
                break
            try:
                first = int(tok)
            except ValueError:
                break
            count_tok = lex.read_token()
            if count_tok is None:
                break
            count = int(count_tok)
            lex.read_line()  # Consomme le reste de la ligne "first count\n"
            for i in range(count):
                line = lex.read_line().strip()
                parts = line.split()
                if len(parts) < 3:
                    continue
                offset_val = int(parts[0])
                gen_num = int(parts[1])
                in_use = parts[2] in (b"n", b"n\r", b"n ")
                obj_num = first + i
                if in_use and obj_num not in self._xref:
                    self._xref[obj_num] = offset_val
                    self._xref_gen[obj_num] = gen_num
        # Lit le trailer
        lex.skip_whitespace_and_comments()
        parser = PDFParser(lex)
        tok2 = lex.read_token()
        if tok2 == b"<<":
            d = parser._parse_dict()
        else:
            d = parser.parse_object()
        if isinstance(d, Mapping) and not self.trailer:
            self.trailer = dict(d)
        elif isinstance(d, Mapping):
            # Merge en gardant les valeurs existantes
            for k, v in d.items():
                if k not in self.trailer:
                    self.trailer[k] = v

    def _parse_xref_stream(self, offset: int) -> None:
        """Parse un xref stream (PDF 1.5+)."""
        lex = PDFLexer(self._data, offset)
        parser = PDFParser(lex)
        # Lit "num gen obj"
        obj_num_tok = lex.read_token()
        gen_tok = lex.read_token()
        obj_kw = lex.read_token()
        if obj_kw != b"obj":
            return
        stream_dict = parser.parse_object()
        if not isinstance(stream_dict, Mapping):
            return
        # Merge le trailer
        if not self.trailer:
            self.trailer = dict(stream_dict)
        else:
            for k, v in stream_dict.items():
                if k not in self.trailer:
                    self.trailer[k] = v
        # Lit "stream\n"
        lex.skip_whitespace_and_comments()
        lex.read_line()  # "stream"
        stream_start = lex.pos
        length = stream_dict.get("Length", 0)
        if isinstance(length, tuple) and length[0] == "ref":
            length = 0  # On essaiera quand même
        length = int(length or 0)
        raw = self._data[stream_start:stream_start + length] if length else self._data[stream_start:stream_start + 65536]
        filters = stream_dict.get("Filter") or stream_dict.get("Filters")
        parms = stream_dict.get("DecodeParms") or stream_dict.get("DecodeParams")
        try:
            stream_data = _decode_stream(raw, filters, parms)
        except Exception:
            return
        # Décode le xref stream
        w = stream_dict.get("W", [1, 1, 1])
        if not isinstance(w, list) or len(w) < 3:
            return
        w = [int(x) for x in w]
        index = stream_dict.get("Index")
        if index is None:
            index = [0, stream_dict.get("Size", 0)]
        if not isinstance(index, list):
            index = [0, int(stream_dict.get("Size", 0))]
        entry_size = sum(w)
        if entry_size == 0:
            return
        entries = [stream_data[i:i+entry_size] for i in range(0, len(stream_data), entry_size)]
        entry_idx = 0
        for pair_idx in range(0, len(index), 2):
            first_obj = int(index[pair_idx])
            count = int(index[pair_idx + 1]) if pair_idx + 1 < len(index) else 0
            for j in range(count):
                if entry_idx >= len(entries):
                    break
                entry = entries[entry_idx]
                entry_idx += 1
                if len(entry) < entry_size:
                    break
                def _read_field(data: bytes, size: int, start: int) -> int:
                    if size == 0:
                        return 1  # default type
                    chunk = data[start:start+size]
                    return int.from_bytes(chunk, "big")
                pos = 0
                f1 = _read_field(entry, w[0], pos); pos += w[0]
                f2 = _read_field(entry, w[1], pos); pos += w[1]
                f3 = _read_field(entry, w[2], pos); pos += w[2]
                obj_num = first_obj + j
                if obj_num in self._xref:
                    continue
                if f1 == 1:  # in-use, f2=offset
                    self._xref[obj_num] = f2
                    self._xref_gen[obj_num] = f3
                elif f1 == 2:  # in object stream, f2=stream_num, f3=index
                    self._xref[obj_num] = -1  # sentinel
                    self._xref_gen[obj_num] = f2 * 65536 + f3  # encode (stream_num, idx)

    # ------------------------------------------------------------------
    # Résolution des objets indirects
    # ------------------------------------------------------------------

    def resolve(self, obj: Any) -> Any:
        """Résout une référence indirecte ("ref", num, gen)."""
        if isinstance(obj, tuple) and len(obj) == 3 and obj[0] == "ref":
            return self._load_object(obj[1])
        return obj

    def _load_object(self, num: int) -> Any:
        if num not in self._xref:
            return None
        offset = self._xref[num]
        if offset == -1:
            # Dans un object stream
            gen_encoded = self._xref_gen.get(num, 0)
            stream_num = gen_encoded // 65536
            obj_idx = gen_encoded % 65536
            return self._load_from_obj_stream(stream_num, obj_idx)
        return self._load_at_offset(offset)

    def _load_at_offset(self, offset: int) -> Any:
        lex = PDFLexer(self._data, offset)
        parser = PDFParser(lex)
        # "num gen obj"
        lex.read_token()  # num
        lex.read_token()  # gen
        kw = lex.read_token()  # "obj"
        if kw != b"obj":
            return None
        obj = parser.parse_object()
        # Si c'est un dict, check si c'est un stream
        lex.skip_whitespace_and_comments()
        peek_tok = lex.read_token()
        if peek_tok == b"stream" and isinstance(obj, dict):
            # Lit le stream
            # Sauter exactement un CRLF ou LF
            if self._data[lex.pos:lex.pos+2] == b"\r\n":
                stream_start = lex.pos + 2
            elif self._data[lex.pos:lex.pos+1] == b"\n":
                stream_start = lex.pos + 1
            else:
                stream_start = lex.pos
            length = self.resolve(obj.get("Length", 0))
            length = int(length or 0) if isinstance(length, (int, float)) else 0
            raw = self._data[stream_start:stream_start + length]
            filters = self.resolve(obj.get("Filter") or obj.get("Filters"))
            parms = self.resolve(obj.get("DecodeParms") or obj.get("DecodeParams"))
            try:
                decoded = _decode_stream(raw, filters, parms)
            except Exception:
                decoded = raw
            obj["__stream__"] = decoded
            obj["__raw_stream__"] = raw
        return obj

    def _load_from_obj_stream(self, stream_num: int, obj_idx: int) -> Any:
        if stream_num in self._obj_stream_cache:
            cache = self._obj_stream_cache[stream_num]
            return list(cache.values())[obj_idx] if obj_idx < len(cache) else None
        stream_obj = self._load_object(stream_num)
        if not isinstance(stream_obj, dict) or "__stream__" not in stream_obj:
            return None
        n = int(stream_obj.get("N", 0))
        first = int(stream_obj.get("First", 0))
        data = stream_obj["__stream__"]
        # Lit les paires "num offset"
        header = data[:first].decode("latin-1", errors="replace")
        pairs = re.findall(r"(\d+)\s+(\d+)", header)
        cache: Dict[int, Any] = {}
        for i, (on, off) in enumerate(pairs[:n]):
            obj_offset = first + int(off)
            lex2 = PDFLexer(data, obj_offset)
            p2 = PDFParser(lex2)
            obj = p2.parse_object()
            cache[int(on)] = obj
        self._obj_stream_cache[stream_num] = cache
        return list(cache.values())[obj_idx] if obj_idx < len(cache) else None

    # ------------------------------------------------------------------
    # Accès aux pages
    # ------------------------------------------------------------------

    def get_pages(self) -> List[Dict[str, Any]]:
        """Retourne la liste ordonnée des objets page du document."""
        root_ref = self.trailer.get("Root")
        if root_ref is None:
            return []
        catalog = self.resolve(root_ref)
        if not isinstance(catalog, dict):
            return []
        pages_ref = catalog.get("Pages")
        if pages_ref is None:
            return []
        pages_obj = self.resolve(pages_ref)
        result: List[Dict[str, Any]] = []
        self._collect_pages(pages_obj, result)
        return result

    def _collect_pages(self, node: Any, result: List[Dict[str, Any]]) -> None:
        if not isinstance(node, dict):
            return
        node_type = self.resolve(node.get("Type", ""))
        if isinstance(node_type, bytes):
            node_type = node_type.decode("latin-1")
        if node_type == "Page":
            result.append(node)
        elif node_type == "Pages":
            kids = self.resolve(node.get("Kids", []))
            if isinstance(kids, list):
                for kid_ref in kids:
                    kid = self.resolve(kid_ref)
                    self._collect_pages(kid, result)

    def get_page_content_streams(self, page: Dict[str, Any]) -> List[bytes]:
        """Récupère les flux de contenu décompressés d'une page."""
        contents = self.resolve(page.get("Contents"))
        if contents is None:
            return []
        if isinstance(contents, list):
            streams = []
            for item in contents:
                obj = self.resolve(item)
                if isinstance(obj, dict) and "__stream__" in obj:
                    streams.append(obj["__stream__"])
            return streams
        if isinstance(contents, dict) and "__stream__" in contents:
            return [contents["__stream__"]]
        return []

    def get_page_fonts(self, page: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """Récupère le dictionnaire des polices de la page (Resources/Font)."""
        resources = self.resolve(page.get("Resources", {}))
        if not isinstance(resources, dict):
            return {}
        font_dict = self.resolve(resources.get("Font", {}))
        if not isinstance(font_dict, dict):
            return {}
        result: Dict[str, Dict[str, Any]] = {}
        for alias, font_ref in font_dict.items():
            font_obj = self.resolve(font_ref)
            if isinstance(font_obj, dict):
                result[alias] = font_obj
        return result


# ---------------------------------------------------------------------------
# Police PDF — décodage en Unicode
# ---------------------------------------------------------------------------

class PDFFont:
    """Gère le décodage des chaînes PDF encodées selon une police."""

    def __init__(self, font_dict: Dict[str, Any], doc: PDFDocument) -> None:
        self._doc = doc
        self._to_unicode: Dict[int, str] = {}
        self._encoding: Dict[int, str] = {}
        self._is_wide = False
        self._parse(font_dict)

    def _parse(self, d: Dict[str, Any]) -> None:
        subtype = self._doc.resolve(d.get("Subtype", ""))
        if isinstance(subtype, bytes):
            subtype = subtype.decode("latin-1")
        self._is_wide = subtype in ("Type0", "CIDFontType0", "CIDFontType2")
        # ToUnicode CMap
        to_unicode_ref = d.get("ToUnicode")
        if to_unicode_ref is not None:
            tu_obj = self._doc.resolve(to_unicode_ref)
            if isinstance(tu_obj, dict) and "__stream__" in tu_obj:
                self._parse_to_unicode(tu_obj["__stream__"])
        if self._to_unicode:
            return
        # Encoding
        enc = self._doc.resolve(d.get("Encoding"))
        if isinstance(enc, str):
            self._load_named_encoding(enc)
        elif isinstance(enc, dict):
            base = self._doc.resolve(enc.get("BaseEncoding", ""))
            if isinstance(base, str):
                self._load_named_encoding(base)
            diffs = self._doc.resolve(enc.get("Differences", []))
            if isinstance(diffs, list):
                self._apply_differences(diffs)
        else:
            self._load_named_encoding("WinAnsiEncoding")

    def _load_named_encoding(self, name: str) -> None:
        name = str(name).strip("/")
        if "WinAnsi" in name or "Win" in name:
            for code, ch in _WINANSI.items():
                self._encoding[code] = ch
        elif "MacRoman" in name:
            try:
                for i in range(256):
                    try:
                        self._encoding[i] = bytes([i]).decode("mac_roman")
                    except Exception:
                        self._encoding[i] = "?"
            except Exception:
                for i in range(32, 128):
                    self._encoding[i] = chr(i)
        else:
            for i in range(32, 128):
                self._encoding[i] = chr(i)

    def _apply_differences(self, diffs: List[Any]) -> None:
        code = 0
        for item in diffs:
            if isinstance(item, (int, float)):
                code = int(item)
            elif isinstance(item, str):
                glyph = item.strip("/")
                if glyph in _GLYPH_TO_UNICODE:
                    self._encoding[code] = _GLYPH_TO_UNICODE[glyph]
                elif len(glyph) == 1:
                    self._encoding[code] = glyph
                elif glyph.startswith("uni") and len(glyph) == 7:
                    try:
                        self._encoding[code] = chr(int(glyph[3:], 16))
                    except ValueError:
                        pass
                elif glyph.startswith("u") and len(glyph) in (5, 6):
                    try:
                        self._encoding[code] = chr(int(glyph[1:], 16))
                    except ValueError:
                        pass
                code += 1

    def _parse_to_unicode(self, data: bytes) -> None:
        """Parse un CMap ToUnicode pour mapper codes -> Unicode.

        Gere correctement les blocs beginbfchar/endbfchar et
        beginbfrange/endbfrange sans chevauchement de regex.
        """
        try:
            text = data.decode("latin-1", errors="replace")
        except Exception:
            return

        # Extrait les blocs beginbfchar...endbfchar
        for block in re.findall(r"beginbfchar\s*(.*?)\s*endbfchar", text, re.DOTALL):
            for m in re.finditer(r"<([0-9A-Fa-f]+)>\s+<([0-9A-Fa-f]+)>", block):
                src_hex, dst_hex = m.group(1), m.group(2)
                try:
                    src_code = int(src_hex, 16)
                    padded = dst_hex if len(dst_hex) % 2 == 0 else "0" + dst_hex
                    dst_text = bytes.fromhex(padded).decode("utf-16-be", errors="replace")
                    self._to_unicode[src_code] = dst_text
                except Exception:
                    pass

        # Extrait les blocs beginbfrange...endbfrange
        for block in re.findall(r"beginbfrange\s*(.*?)\s*endbfrange", text, re.DOTALL):
            for m in re.finditer(
                r"<([0-9A-Fa-f]+)>\s+<([0-9A-Fa-f]+)>\s+<([0-9A-Fa-f]+)>", block
            ):
                s_hex, e_hex, d_hex = m.group(1), m.group(2), m.group(3)
                try:
                    s = int(s_hex, 16)
                    e = int(e_hex, 16)
                    padded = d_hex if len(d_hex) % 2 == 0 else "0" + d_hex
                    d_bytes = bytes.fromhex(padded)
                    if len(d_bytes) >= 2:
                        d_cp = int.from_bytes(d_bytes, "big")
                        for i in range(e - s + 1):
                            self._to_unicode[s + i] = chr(d_cp + i)
                except Exception:
                    pass

        # Fallback sans blocs explicites
        if not self._to_unicode:
            for m in re.finditer(
                r"<([0-9A-Fa-f]{2,4})>\s+<([0-9A-Fa-f]{4})>(?!\s*<)",
                text
            ):
                src_hex, dst_hex = m.group(1), m.group(2)
                try:
                    src_code = int(src_hex, 16)
                    dst_text = bytes.fromhex(dst_hex).decode("utf-16-be", errors="replace")
                    self._to_unicode[src_code] = dst_text
                except Exception:
                    pass

    def decode(self, raw: bytes) -> str:
        """Décode des bytes en texte Unicode via la police."""
        if not raw:
            return ""
        result = []
        if self._to_unicode:
            if self._is_wide:
                i = 0
                while i + 1 < len(raw):
                    code = (raw[i] << 8) | raw[i + 1]
                    i += 2
                    ch = self._to_unicode.get(code)
                    if ch is None:
                        ch = self._to_unicode.get(raw[i - 2], "?")
                    result.append(ch or "?")
                if i < len(raw):
                    result.append(self._to_unicode.get(raw[i], "?"))
            else:
                for b in raw:
                    ch = self._to_unicode.get(b)
                    result.append(ch if ch is not None else self._to_unicode.get(b, "?"))
        elif self._encoding:
            for b in raw:
                result.append(self._encoding.get(b, chr(b) if 32 <= b < 128 else "?"))
        else:
            try:
                return raw.decode("utf-8")
            except UnicodeDecodeError:
                return raw.decode("latin-1", errors="replace")
        return "".join(result)


# ---------------------------------------------------------------------------
# Extraction de texte depuis flux de contenu
# ---------------------------------------------------------------------------

class PDFContentParser:
    """Extrait le texte depuis un flux de contenu PDF."""

    def __init__(self, doc: PDFDocument, fonts: Dict[str, PDFFont]) -> None:
        self._doc = doc
        self._fonts = fonts
        self._current_font: Optional[PDFFont] = None
        self._font_size: float = 12.0
        self._char_spacing: float = 0.0
        self._word_spacing: float = 0.0
        self._text_rise: float = 0.0
        self._text_mode: bool = False
        self._x: float = 0.0
        self._y: float = 0.0
        self._prev_y: float = 0.0
        self._line_parts: List[str] = []
        self._lines: List[str] = []

    def extract(self, streams: List[bytes]) -> str:
        """Extrait tout le texte d'une liste de flux de contenu de page."""
        self._line_parts = []
        self._lines = []
        self._text_mode = False
        for stream in streams:
            self._process_stream(stream)
        self._flush_line()
        return "\n".join(l for l in self._lines if l.strip())

    def _process_stream(self, data: bytes) -> None:
        lex = PDFLexer(data)
        parser = PDFParser(lex)
        stack: List[Any] = []
        while True:
            lex.skip_whitespace_and_comments()
            if lex.pos >= len(data):
                break
            try:
                tok = lex.read_token()
            except Exception:
                break
            if tok is None:
                break
            # Tente de parser comme objet
            if tok == b">>":
                stack.append(">>")
                continue
            if tok == b"<<":
                d = parser._parse_dict()
                stack.append(d)
                continue
            # Opérateurs texte
            if tok == b"BT":
                self._text_mode = True
                self._x = 0.0
                self._y = 0.0
            elif tok == b"ET":
                self._text_mode = False
                self._flush_line()
            elif tok == b"Tf":
                if len(stack) >= 2:
                    size = stack.pop()
                    font_alias = stack.pop()
                    if isinstance(font_alias, str):
                        font_alias = font_alias.strip("/")
                    self._current_font = self._fonts.get(str(font_alias))
                    try:
                        self._font_size = float(size)
                    except Exception:
                        pass
                    stack.clear()
            elif tok == b"Td":
                if len(stack) >= 2:
                    ty = stack.pop()
                    tx = stack.pop()
                    try:
                        self._y += float(ty)
                        self._x += float(tx)
                    except Exception:
                        pass
                    stack.clear()
                    if abs(float(ty if isinstance(ty, (int, float)) else 0)) > 0.5:
                        self._flush_line()
            elif tok == b"TD":
                if len(stack) >= 2:
                    ty = stack.pop()
                    tx = stack.pop()
                    try:
                        self._word_spacing = -float(ty if isinstance(ty, (int, float)) else 0)
                        self._y += float(ty if isinstance(ty, (int, float)) else 0)
                        self._x += float(tx if isinstance(tx, (int, float)) else 0)
                    except Exception:
                        pass
                    stack.clear()
                    self._flush_line()
            elif tok == b"Tm":
                if len(stack) >= 6:
                    f = stack[-6:]
                    stack = stack[:-6]
                    try:
                        new_y = float(f[5])
                        if abs(new_y - self._y) > 1.0:
                            self._flush_line()
                        self._y = new_y
                        self._x = float(f[4])
                    except Exception:
                        pass
            elif tok in (b"T*", b"'"):
                self._flush_line()
                if tok == b"'" and stack:
                    self._show_string(stack.pop())
                    stack.clear()
            elif tok == b'"':
                if len(stack) >= 3:
                    s = stack.pop()
                    stack.pop()  # word spacing
                    stack.pop()  # char spacing
                    self._flush_line()
                    self._show_string(s)
                    stack.clear()
            elif tok == b"Tj":
                if stack:
                    self._show_string(stack.pop())
                    stack.clear()
            elif tok == b"TJ":
                if stack:
                    arr = stack.pop()
                    stack.clear()
                    if isinstance(arr, list):
                        for item in arr:
                            if isinstance(item, bytes):
                                self._show_string(item)
                            elif isinstance(item, (int, float)) and abs(item) > 200:
                                # Grand kerning négatif → espace
                                self._line_parts.append(" ")
                    elif isinstance(arr, bytes):
                        self._show_string(arr)
            elif tok == b"Tc":
                if stack:
                    try:
                        self._char_spacing = float(stack.pop())
                    except Exception:
                        stack.pop()
                    stack.clear()
            elif tok == b"Tw":
                if stack:
                    try:
                        self._word_spacing = float(stack.pop())
                    except Exception:
                        stack.pop()
                    stack.clear()
            elif tok in (b"cm", b"q", b"Q", b"re", b"w", b"J", b"j",
                         b"M", b"d", b"ri", b"i", b"gs", b"Do", b"cs",
                         b"CS", b"sc", b"SC", b"scn", b"SCN", b"g", b"G",
                         b"rg", b"RG", b"k", b"K", b"sh", b"W", b"W*",
                         b"n", b"S", b"s", b"f", b"F", b"f*", b"B", b"B*",
                         b"b", b"b*", b"m", b"l", b"c", b"v", b"y", b"h",
                         b"BI", b"ID", b"EI", b"BMC", b"BDC", b"EMC",
                         b"MP", b"DP"):
                stack.clear()
            else:
                # Tente de pousser sur la pile comme valeur
                try:
                    val = parser._parse_token(tok)
                    stack.append(val)
                except Exception:
                    stack.clear()

    def _show_string(self, s: Any) -> None:
        if isinstance(s, bytes) and self._current_font:
            text = self._current_font.decode(s)
        elif isinstance(s, bytes):
            try:
                text = s.decode("utf-8")
            except UnicodeDecodeError:
                text = s.decode("latin-1", errors="replace")
        elif isinstance(s, str):
            text = s
        else:
            return
        if text:
            self._line_parts.append(text)

    def _flush_line(self) -> None:
        if self._line_parts:
            line = "".join(self._line_parts).strip()
            if line:
                self._lines.append(line)
            self._line_parts = []


# ---------------------------------------------------------------------------
# Interface principale — remplacement de LeiaPDFKnowledgeEngine
# ---------------------------------------------------------------------------

class LeiaPurePDFReader:
    """
    Lecteur PDF pur Python, zéro dépendance externe.

    Remplace et complète LeiaPDFKnowledgeEngine en parsant le format PDF
    directement depuis les octets, sans pypdf ni PyPDF2.

    Interface identique à LeiaPDFKnowledgeEngine pour permettre un swap
    transparent dans leia_living_core.py.
    """

    def __init__(
        self,
        memory_system: Any = None,
        digestion_engine: Any = None,
        progress_callback: Optional[ProgressCallback] = None,
        max_chars_per_chunk: int = 1800,
        pause_between_chunks: float = 0.005,
    ) -> None:
        self.memory_system = memory_system
        self.digestion_engine = digestion_engine
        self.progress_callback = progress_callback
        self.max_chars_per_chunk = max(500, int(max_chars_per_chunk or 1800))
        self.pause_between_chunks = max(0.0, float(pause_between_chunks or 0.0))
        self.cancel_requested = False

    def set_progress_callback(self, callback: Optional[ProgressCallback]) -> None:
        self.progress_callback = callback

    def request_cancel(self) -> None:
        self.cancel_requested = True

    # ------------------------------------------------------------------
    # Logs
    # ------------------------------------------------------------------

    def _log(self, message: str) -> None:
        msg = f"[PDF-NATIF] {message}"
        try:
            print(msg, flush=True)
        except Exception:
            pass
        if self.progress_callback:
            try:
                self.progress_callback(msg)
            except Exception:
                pass

    # ------------------------------------------------------------------
    # Découpage du texte en fragments
    # ------------------------------------------------------------------

    def _split_text(self, text: str) -> List[str]:
        text = " ".join((text or "").split())
        if not text:
            return []
        chunks: List[str] = []
        start = 0
        n = len(text)
        while start < n:
            end = min(n, start + self.max_chars_per_chunk)
            if end < n:
                boundaries = [
                    text.rfind(". ", start, end),
                    text.rfind("? ", start, end),
                    text.rfind("! ", start, end),
                    text.rfind("; ", start, end),
                    text.rfind(": ", start, end),
                ]
                boundary = max(boundaries)
                if boundary > start + 350:
                    end = boundary + 1
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            if end <= start:
                break
            start = end
        return chunks

    # ------------------------------------------------------------------
    # Pipeline de digestion et mémoire (repris de pdf_knowledge_engine)
    # ------------------------------------------------------------------

    def _call_digestion(self, text: str, page: int, chunk_index: int) -> Dict[str, Any]:
        if not self.digestion_engine:
            return {"available": False, "resonance": 0.0, "curiosity": 0.0, "friction": 0.0}
        payload = {"text": text, "page": page, "chunk_index": chunk_index, "source": "pdf"}
        for name in ("digest_text", "digest", "process_text", "ingest_text", "digest_knowledge", "learn_text"):
            fn = getattr(self.digestion_engine, name, None)
            if not callable(fn):
                continue
            try:
                result = fn(text)
            except TypeError:
                try:
                    result = fn(payload)
                except Exception as exc:
                    return {"available": True, "error": f"{type(exc).__name__}: {exc}", "method": name}
            except Exception as exc:
                return {"available": True, "error": f"{type(exc).__name__}: {exc}", "method": name}
            out = _jsonable(result)
            if isinstance(out, Mapping):
                out = dict(out)
                out.setdefault("available", True)
                out.setdefault("method", name)
                return out
            return {"available": True, "method": name, "raw": str(out)[:400]}
        return {"available": False, "reason": "no compatible digestion method"}

    def _digestion_counts(self, digestion: Mapping[str, Any]) -> Dict[str, int]:
        traces = digestion.get("traces", []) if isinstance(digestion, Mapping) else []
        return {
            "traces": len(traces) if isinstance(traces, list) else 0,
            "atoms": int(digestion.get("atoms_created", 0) or 0) if isinstance(digestion, Mapping) else 0,
            "neurons_created": int(digestion.get("neurons_created", 0) or 0) if isinstance(digestion, Mapping) else 0,
            "neurons_reinforced": int(digestion.get("neurons_reinforced", 0) or 0) if isinstance(digestion, Mapping) else 0,
            "links_created": int(digestion.get("links_created", 0) or 0) if isinstance(digestion, Mapping) else 0,
        }

    def _store_memory(self, trace: Dict[str, Any]) -> bool:
        if not self.memory_system:
            return False
        text = str(trace.get("text", "")).strip()
        if not text:
            return False
        digestion = trace.get("digestion", {}) if isinstance(trace.get("digestion"), Mapping) else {}
        counts = self._digestion_counts(digestion)
        source_file = str(trace.get("source_file", "PDF"))
        page = trace.get("page", "?")
        chunk = trace.get("chunk_index", "?")
        excerpt = text[:420]
        learn = getattr(self.memory_system, "learn_causal_relation", None)
        if callable(learn):
            try:
                learn(
                    event=f"Lecture du PDF {source_file}, page {page}, fragment {chunk}: {excerpt}",
                    experienced_effect=(
                        "Consolide une connaissance de livre en mémoire active: "
                        f"{counts['atoms']} atomes, {counts['neurons_created']} neurones nouveaux, "
                        f"{counts['neurons_reinforced']} renforcements, {counts['links_created']} liens."
                    ),
                    emotional_trace="curious",
                    behavioral_shift="réactiver les concepts lus quand l'utilisateur questionne le livre",
                    attention_impact="augmenter l'attention sur mémoire, matière, esprit, perception et action si présents",
                    source_context={
                        "type": "pdf_knowledge",
                        "source_file": source_file,
                        "source_path": trace.get("source_path", ""),
                        "page": page,
                        "chunk_index": chunk,
                        "excerpt": excerpt,
                        "digestion_counts": counts,
                    },
                    initial_confidence=0.66,
                    memory_kind="initiative_learning",
                    valence=0.18,
                    effect_strength=min(1.0, 0.35 + counts["atoms"] * 0.035 + counts["links_created"] * 0.01),
                    recurrence_pressure=0.22,
                    source_engine="leia_pure_pdf_reader",
                    identity_impact=0.18,
                    autobiographical_weight=0.14,
                    causal_layers={
                        "book_learning": 0.82,
                        "semantic_consolidation": min(1.0, 0.3 + counts["atoms"] * 0.04),
                        "dialogue_reactivation": 0.72,
                    },
                    episode_context={"origin": "pdf_reading", "page": page, "chunk": chunk},
                )
                return True
            except TypeError:
                try:
                    learn(
                        f"Lecture du PDF {source_file}, page {page}: {excerpt}",
                        "Connaissance de livre consolidée pour réactivation en dialogue.",
                    )
                    return True
                except Exception:
                    pass
            except Exception:
                pass
        for name in ("store_memory", "remember", "add_memory", "store", "save_memory", "record", "append"):
            fn = getattr(self.memory_system, name, None)
            if not callable(fn):
                continue
            try:
                fn(trace)
                return True
            except TypeError:
                try:
                    fn(text, metadata={k: v for k, v in trace.items() if k != "text"})
                    return True
                except Exception:
                    continue
            except Exception:
                continue
        return False

    # ------------------------------------------------------------------
    # Point d'entrée principal
    # ------------------------------------------------------------------

    def read_pdf(
        self,
        pdf_path: str,
        *,
        progress_callback: Optional[ProgressCallback] = None,
        max_pages: Optional[int] = None,
        start_page: int = 1,
        preview_limit: int = 20,
    ) -> Dict[str, Any]:
        if progress_callback is not None:
            self.progress_callback = progress_callback
        self.cancel_requested = False

        path = Path(pdf_path).expanduser()
        if not path.exists():
            return {"success": False, "error": f"Fichier introuvable: {path}"}

        self._log(f"chargement binaire: {path} ({path.stat().st_size:,} octets)")

        try:
            raw_data = path.read_bytes()
        except Exception as exc:
            return {"success": False, "error": f"Lecture impossible: {exc}"}

        if not raw_data.startswith(b"%PDF"):
            return {"success": False, "error": "Ce fichier n'est pas un PDF valide (header %PDF absent)"}

        self._log(f"parsing de la structure PDF...")
        try:
            doc = PDFDocument(raw_data)
        except PDFParseError as exc:
            return {"success": False, "error": f"Structure PDF invalide: {exc}"}
        except Exception as exc:
            return {"success": False, "error": f"Erreur de parsing: {type(exc).__name__}: {exc}"}

        if doc.encrypted:
            return {
                "success": False,
                "error": "PDF chiffré — déchiffrement non supporté dans le lecteur natif",
            }

        self._log("récupération des pages...")
        try:
            pages = doc.get_pages()
        except Exception as exc:
            return {"success": False, "error": f"Impossible d'accéder aux pages: {exc}"}

        total_pages = len(pages)
        if total_pages == 0:
            return {"success": False, "error": "Aucune page trouvée dans ce PDF"}

        start_page = max(1, int(start_page or 1))
        if max_pages is None:
            end_page = total_pages
        else:
            end_page = min(total_pages, start_page + max(1, int(max_pages)) - 1)

        self._log(f"{total_pages} pages détectées. Lecture pages {start_page} à {end_page}.")

        pages_read = 0
        chunks_created = 0
        memory_traces = 0
        errors: List[str] = []
        preview: List[Dict[str, Any]] = []

        for page_number in range(start_page, end_page + 1):
            if self.cancel_requested:
                self._log("annulation demandée")
                break

            self._log(f"extraction page {page_number}/{total_pages}")
            page = pages[page_number - 1]

            try:
                # Construction des polices de la page
                raw_fonts = doc.get_page_fonts(page)
                fonts: Dict[str, PDFFont] = {}
                for alias, font_dict in raw_fonts.items():
                    try:
                        fonts[alias] = PDFFont(font_dict, doc)
                    except Exception:
                        pass

                # Extraction du texte
                content_streams = doc.get_page_content_streams(page)
                extractor = PDFContentParser(doc, fonts)
                text = extractor.extract(content_streams)
            except Exception as exc:
                error = f"page {page_number}: {type(exc).__name__}: {exc}"
                errors.append(error)
                self._log(error)
                continue

            text = text.strip()
            if not text:
                self._log(f"page {page_number}: aucun texte extractible")
                continue

            pages_read += 1
            fragments = self._split_text(text)
            self._log(f"page {page_number}: {len(fragments)} fragments")

            for chunk_index, fragment in enumerate(fragments, 1):
                if self.cancel_requested:
                    break

                self._log(f"digestion page {page_number}, fragment {chunk_index}/{len(fragments)}")
                digestion = self._call_digestion(fragment, page_number, chunk_index)

                trace = {
                    "type": "pdf_knowledge",
                    "source_file": path.name,
                    "source_path": str(path),
                    "page": page_number,
                    "chunk_index": chunk_index,
                    "text": fragment,
                    "digestion": digestion,
                    "created_at": time.time(),
                }

                stored = self._store_memory(trace)
                if stored:
                    memory_traces += 1
                chunks_created += 1

                if len(preview) < preview_limit:
                    preview.append({
                        "page": page_number,
                        "chunk_index": chunk_index,
                        "text_preview": fragment[:260],
                        "digestion": digestion,
                        "stored": stored,
                    })

                if self.pause_between_chunks:
                    time.sleep(self.pause_between_chunks)

        # Synthèse conceptuelle finale
        conceptual_synthesis: Dict[str, Any] = {"available": False}
        if self.digestion_engine is not None:
            build = getattr(self.digestion_engine, "build_conceptual_synthesis", None)
            if callable(build):
                try:
                    conceptual_synthesis = build(
                        context_text=path.stem,
                        source_hint=str(path),
                        limit=14,
                    )
                except Exception as exc:
                    conceptual_synthesis = {"available": False, "error": f"{type(exc).__name__}: {exc}"}

        self._log(
            f"terminé: {pages_read} pages lues, {chunks_created} fragments, "
            f"{memory_traces} traces mémoire"
        )

        return {
            "success": True,
            "file": str(path),
            "total_pages": total_pages,
            "start_page": start_page,
            "end_page": end_page,
            "pages_read": pages_read,
            "chunks_count": chunks_created,
            "memory_traces": memory_traces,
            "conceptual_synthesis": conceptual_synthesis,
            "errors": errors,
            "traces_preview": preview,
            "preview_truncated": chunks_created > len(preview),
            "reader": "LeiaPurePDFReader (natif, zéro dépendance externe)",
        }

    # ------------------------------------------------------------------
    # Utilitaire standalone — extraction de texte simple
    # ------------------------------------------------------------------

    @staticmethod
    def extract_text_only(pdf_path: str) -> Dict[str, Any]:
        """
        Extrait tout le texte d'un PDF sans pipeline de digestion.
        Usage : LeiaPurePDFReader.extract_text_only("/chemin/livre.pdf")
        Retourne : {"success": True, "pages": [{"page": 1, "text": "..."}], ...}
        """
        path = Path(pdf_path).expanduser()
        if not path.exists():
            return {"success": False, "error": f"Fichier introuvable: {path}"}
        try:
            raw_data = path.read_bytes()
        except Exception as exc:
            return {"success": False, "error": str(exc)}
        if not raw_data.startswith(b"%PDF"):
            return {"success": False, "error": "Header %PDF absent"}
        try:
            doc = PDFDocument(raw_data)
        except Exception as exc:
            return {"success": False, "error": str(exc)}
        if doc.encrypted:
            return {"success": False, "error": "PDF chiffré"}
        pages_obj = doc.get_pages()
        result_pages = []
        for i, page in enumerate(pages_obj, 1):
            try:
                raw_fonts = doc.get_page_fonts(page)
                fonts = {}
                for alias, fd in raw_fonts.items():
                    try:
                        fonts[alias] = PDFFont(fd, doc)
                    except Exception:
                        pass
                streams = doc.get_page_content_streams(page)
                text = PDFContentParser(doc, fonts).extract(streams)
                result_pages.append({"page": i, "text": text.strip()})
            except Exception as exc:
                result_pages.append({"page": i, "text": "", "error": str(exc)})
        full_text = "\n\n".join(p["text"] for p in result_pages if p.get("text"))
        return {
            "success": True,
            "file": str(path),
            "total_pages": len(result_pages),
            "pages": result_pages,
            "full_text": full_text,
            "chars": len(full_text),
        }

    @staticmethod
    def get_info(pdf_path: str) -> Dict[str, Any]:
        """
        Infos rapides sans extraction de texte complète.
        Retourne : version PDF, nombre de pages, chiffrement, taille.
        """
        path = Path(pdf_path).expanduser()
        if not path.exists():
            return {"success": False, "error": f"Fichier introuvable: {path}"}
        try:
            raw = path.read_bytes()
        except Exception as exc:
            return {"success": False, "error": str(exc)}
        header_match = re.match(rb"%PDF-(\d+\.\d+)", raw[:16])
        version = header_match.group(1).decode() if header_match else "?"
        try:
            doc = PDFDocument(raw)
            pages = doc.get_pages()
            return {
                "success": True,
                "file": str(path),
                "size_bytes": len(raw),
                "pdf_version": version,
                "total_pages": len(pages),
                "encrypted": doc.encrypted,
            }
        except Exception as exc:
            return {"success": False, "error": str(exc), "pdf_version": version}


# ---------------------------------------------------------------------------
# Alias de compatibilité — permet un swap transparent dans leia_living_core
# ---------------------------------------------------------------------------

# Si pypdf/PyPDF2 est absent, LeiaPurePDFReader remplace silencieusement
# LeiaPDFKnowledgeEngine via ce nom :
LeiaNativePDFEngine = LeiaPurePDFReader


# ---------------------------------------------------------------------------
# CLI minimal pour tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    args = sys.argv[1:]
    if not args:
        print("Usage: python leia_pure_pdf_reader.py <fichier.pdf> [--info] [--texte] [--pages N]")
        sys.exit(0)

    pdf_file = args[0]
    mode = "--info" if "--info" in args else ("--texte" if "--texte" in args else "--texte")
    max_p = None
    if "--pages" in args:
        idx = args.index("--pages")
        if idx + 1 < len(args):
            max_p = int(args[idx + 1])

    if mode == "--info":
        info = LeiaPurePDFReader.get_info(pdf_file)
        print(json.dumps(info, ensure_ascii=False, indent=2))
    else:
        result = LeiaPurePDFReader.extract_text_only(pdf_file)
        if not result["success"]:
            print("ERREUR:", result.get("error"))
            sys.exit(1)
        print(f"=== {result['file']} — {result['total_pages']} pages — {result['chars']:,} caractères ===\n")
        pages_to_show = result["pages"]
        if max_p:
            pages_to_show = pages_to_show[:max_p]
        for p in pages_to_show:
            print(f"--- Page {p['page']} ---")
            print(p.get("text", "")[:2000])
            print()


# ===========================================================================
# INTÉGRATION V20 — SemanticCortex + GlobalWorkspace
# ===========================================================================
#
# Ce bloc ajoute le pipeline V20 au-dessus du parseur binaire existant.
# Il ne modifie rien à la mécanique de parsing PDF — seule la couche
# de compréhension change : on passe de l'ancienne digestion
# émotionnelle vers SemanticCortex → CognitiveStructure → workspace.
#
# Usage dans leia_unified_connector.py :
#
#   from leia_pure_pdf_reader import LeiaPDFV20Connector
#
#   class LeiaLivingCore:
#       def __init__(self, ...):
#           ...
#           self.pdf_connector = LeiaPDFV20Connector(
#               cortex=self.cortex,      # SemanticCortex
#               workspace=self.workspace # GlobalWorkspace / CognitiveWorkspace
#           )
#
#       def load_pdf_book(self, path, progress_callback=None, ...):
#           return self.pdf_connector.load_pdf_book(path, progress_callback, ...)
#
# ===========================================================================

class LeiaPDFV20Connector:
    """
    Lecteur PDF V20 — zéro dépendance externe, pipeline SemanticCortex.

    Architecture :
        Bytes PDF
            ↓  LeiaPurePDFReader (parseur natif pur Python)
        Texte page par page
            ↓  SemanticCortex.process(fragment)
        CognitiveStructure
            ↓  workspace.ingest_structure(structure)
        Graphe causal vivant + tensions + scènes actives

    Ce connecteur remplace le stub `load_pdf_book()` de leia_unified_connector.py.
    Il est rétrocompatible avec l'ancienne interface V19 :
    les arguments `memory_system` et `digestion_engine` sont acceptés mais ignorés
    si `workspace` et `cortex` sont fournis.
    """

    def __init__(
        self,
        cortex: Any = None,
        workspace: Any = None,
        # V19 compat
        memory_system: Any = None,
        digestion_engine: Any = None,
        progress_callback: Optional[ProgressCallback] = None,
        max_chars_per_chunk: int = 1800,
        pause_between_chunks: float = 0.003,
    ) -> None:
        # Nouveaux moteurs V20
        self.cortex = cortex
        self.workspace = workspace

        # Fallback V19 si workspace absent
        self._v19_memory = memory_system
        self._v19_digestion = digestion_engine

        self.progress_callback = progress_callback
        self.max_chars_per_chunk = max(500, int(max_chars_per_chunk or 1800))
        self.pause_between_chunks = max(0.0, float(pause_between_chunks or 0.0))
        self.cancel_requested = False

        # Lecteur binaire — partagé entre V19 et V20
        self._reader = LeiaPurePDFReader(
            memory_system=memory_system,
            digestion_engine=digestion_engine,
            max_chars_per_chunk=max_chars_per_chunk,
            pause_between_chunks=pause_between_chunks,
        )

        # Résumé de session
        self._last_session: Dict[str, Any] = {}

    def set_progress_callback(self, cb: Optional[ProgressCallback]) -> None:
        self.progress_callback = cb
        self._reader.progress_callback = cb

    def request_cancel(self) -> None:
        self.cancel_requested = True
        self._reader.cancel_requested = True

    # ------------------------------------------------------------------
    # Interface principale — identique à load_pdf_book() du connector
    # ------------------------------------------------------------------

    def load_pdf_book(
        self,
        path: str,
        progress_callback: Optional[ProgressCallback] = None,
        max_pages: Optional[int] = None,
        start_page: int = 1,
    ) -> Dict[str, Any]:
        """
        Charge et digère un PDF dans le système V20.
        Retourne un rapport complet compatible avec l'interface Tkinter.

        Le rapport inclut :
            ok, file, total_pages, pages_read, chunks_count,
            cognitive_structures, workspace_integrations, errors,
            traces_preview, reader
        """
        if progress_callback is not None:
            self.set_progress_callback(progress_callback)
        self.cancel_requested = False
        self._reader.cancel_requested = False

        path_obj = Path(path).expanduser()
        if not path_obj.exists():
            return {"ok": False, "error": f"Fichier introuvable : {path}"}

        self._log(f"ouverture : {path_obj} ({path_obj.stat().st_size:,} octets)")

        # --- Chargement et parsing du PDF ---
        try:
            raw = path_obj.read_bytes()
        except Exception as exc:
            return {"ok": False, "error": f"Lecture impossible : {exc}"}

        if not raw.startswith(b"%PDF"):
            return {"ok": False, "error": "Ce fichier n'est pas un PDF (header %PDF absent)"}

        self._log("parsing de la structure PDF...")
        try:
            doc = PDFDocument(raw)
        except PDFParseError as exc:
            return {"ok": False, "error": f"Structure PDF invalide : {exc}"}
        except Exception as exc:
            return {"ok": False, "error": f"Erreur parsing : {type(exc).__name__} : {exc}"}

        if doc.encrypted:
            return {"ok": False, "error": "PDF chiffré — déchiffrement non supporté"}

        self._log("récupération des pages...")
        try:
            pages = doc.get_pages()
        except Exception as exc:
            return {"ok": False, "error": f"Impossible d'accéder aux pages : {exc}"}

        total_pages = len(pages)
        if total_pages == 0:
            return {"ok": False, "error": "Aucune page trouvée dans ce PDF"}

        start_page = max(1, int(start_page or 1))
        end_page = total_pages if max_pages is None else min(
            total_pages, start_page + max(1, int(max_pages)) - 1
        )

        self._log(f"{total_pages} pages détectées — lecture pages {start_page} à {end_page}")

        # --- Extraction + pipeline V20 ---
        pages_read = 0
        chunks_done = 0
        cognitive_structures = 0
        workspace_integrations = 0
        errors: List[str] = []
        preview: List[Dict[str, Any]] = []
        PREVIEW_LIMIT = 16

        for page_num in range(start_page, end_page + 1):
            if self.cancel_requested:
                self._log("annulation demandée")
                break

            self._log(f"extraction page {page_num}/{total_pages}")
            page = pages[page_num - 1]

            try:
                raw_fonts = doc.get_page_fonts(page)
                fonts: Dict[str, "PDFFont"] = {}
                for alias, fd in raw_fonts.items():
                    try:
                        fonts[alias] = PDFFont(fd, doc)
                    except Exception:
                        pass
                streams = doc.get_page_content_streams(page)
                text = PDFContentParser(doc, fonts).extract(streams).strip()
            except Exception as exc:
                err = f"page {page_num} : {type(exc).__name__} : {exc}"
                errors.append(err)
                self._log(err)
                continue

            if not text:
                self._log(f"page {page_num} : aucun texte extractible")
                continue

            pages_read += 1
            fragments = self._reader._split_text(text)
            self._log(f"page {page_num} : {len(fragments)} fragment(s)")

            for frag_idx, fragment in enumerate(fragments, 1):
                if self.cancel_requested:
                    break

                self._log(f"compréhension page {page_num}, fragment {frag_idx}/{len(fragments)}")

                # Passe par SemanticCortex si disponible → structure cognitive
                cs_dict: Dict[str, Any] = {"available": False}
                cs_obj = None

                if self.cortex is not None:
                    try:
                        cs_obj = self.cortex.process(fragment, source=path_obj.name)
                        cs_dict = _jsonable(cs_obj.to_dict()) if hasattr(cs_obj, "to_dict") else _jsonable(cs_obj)
                        cs_dict["available"] = True
                        cognitive_structures += 1
                    except Exception as exc:
                        cs_dict = {"available": False, "error": f"{type(exc).__name__} : {exc}"}

                # Injecte dans le workspace
                if self.workspace is not None and cs_obj is not None:
                    try:
                        # CognitiveWorkspace (integration_cortex_workspace) expose ingest_structure()
                        ingest = getattr(self.workspace, "ingest_structure", None)
                        if callable(ingest):
                            ingest(cs_obj, source=path_obj.name)
                            workspace_integrations += 1
                        else:
                            # Fallback : inject_perception (GlobalWorkspace V2)
                            inject = getattr(self.workspace, "inject_perception", None)
                            if callable(inject):
                                inject({"text": fragment, "source": path_obj.name, "page": page_num})
                                workspace_integrations += 1
                    except Exception as exc:
                        errors.append(f"workspace page {page_num} : {type(exc).__name__} : {exc}")

                # Fallback V19 si pas de V20
                elif self.cortex is None:
                    self._reader._call_digestion(fragment, page_num, frag_idx)
                    trace = {
                        "type": "pdf_knowledge",
                        "source_file": path_obj.name,
                        "source_path": str(path_obj),
                        "page": page_num,
                        "chunk_index": frag_idx,
                        "text": fragment,
                        "created_at": time.time(),
                    }
                    self._reader._store_memory(trace)

                chunks_done += 1

                if len(preview) < PREVIEW_LIMIT:
                    preview.append({
                        "page": page_num,
                        "fragment": frag_idx,
                        "text_preview": fragment[:240],
                        "cognitive_structure": cs_dict,
                        "workspace_ingested": workspace_integrations > 0,
                    })

                if self.pause_between_chunks:
                    time.sleep(self.pause_between_chunks)

        # Synthèse post-lecture
        post_synthesis: Dict[str, Any] = {"available": False}
        if self.workspace is not None:
            try:
                # Signal de fin de lecture au workspace
                signal_fn = getattr(self.workspace, "signal_lecture_terminee", None)
                if callable(signal_fn):
                    post_synthesis = signal_fn(source=path_obj.name) or {"available": True, "done": True}
                else:
                    # Essai via tick() pour déclencher une pensée spontanée
                    tick_fn = getattr(self.workspace, "tick", None)
                    if callable(tick_fn):
                        tick_fn()
                    post_synthesis = {"available": True, "workspace_ticked": True}
            except Exception as exc:
                post_synthesis = {"available": False, "error": str(exc)}

        self._log(
            f"terminé : {pages_read} pages, {chunks_done} fragments, "
            f"{cognitive_structures} structures cognitives, "
            f"{workspace_integrations} intégrations workspace"
        )

        result = {
            "ok": True,
            "success": True,  # compat V19
            "file": str(path_obj),
            "total_pages": total_pages,
            "start_page": start_page,
            "end_page": end_page,
            "pages_read": pages_read,
            "chunks_count": chunks_done,
            "cognitive_structures": cognitive_structures,
            "workspace_integrations": workspace_integrations,
            "post_synthesis": post_synthesis,
            "errors": errors,
            "traces_preview": preview,
            "reader": "LeiaPDFV20Connector (natif V20, zéro dépendance)",
            "pipeline": "SemanticCortex → CognitiveStructure → workspace.ingest_structure"
            if self.cortex and self.workspace
            else "V19 compat (pas de cortex/workspace fournis)",
        }

        self._last_session = result
        return result

    def get_last_session(self) -> Dict[str, Any]:
        """Retourne le rapport de la dernière session de lecture."""
        return self._last_session.copy()

    def _log(self, message: str) -> None:
        msg = f"[PDF-V20] {message}"
        try:
            print(msg, flush=True)
        except Exception:
            pass
        if self.progress_callback:
            try:
                self.progress_callback(msg)
            except Exception:
                pass


# ---------------------------------------------------------------------------
# Patch drop-in pour leia_unified_connector.py
# ---------------------------------------------------------------------------
#
# Dans leia_unified_connector.py, remplace le stub :
#
#   def load_pdf_book(self, path, progress_callback=None, max_pages=None, start_page=1):
#       """Stub — la digestion PDF nécessiterait des libs externes."""
#       return {"ok": False, "error": "PDF non connecté dans cette version unifiée", "path": path}
#
# Par :
#
#   # En haut du fichier :
#   try:
#       from leia_pure_pdf_reader import LeiaPDFV20Connector
#       _PDF_V20_OK = True
#   except Exception:
#       _PDF_V20_OK = False
#
#   # Dans __init__ :
#   self._pdf = LeiaPDFV20Connector(
#       cortex=getattr(self, "cortex", None),
#       workspace=self.workspace,
#   ) if _PDF_V20_OK else None
#
#   # Méthode réelle :
#   def load_pdf_book(self, path, progress_callback=None, max_pages=None, start_page=1):
#       if self._pdf is None:
#           return {"ok": False, "error": "LeiaPDFV20Connector non disponible"}
#       return self._pdf.load_pdf_book(
#           path, progress_callback=progress_callback,
#           max_pages=max_pages, start_page=start_page
#       )
#
# ---------------------------------------------------------------------------
