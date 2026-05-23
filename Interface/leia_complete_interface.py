#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Leia Complete Interface — V19 REDESIGN
Interface graphique complète, moderne et élégante pour Leia.
"""

from __future__ import annotations

import json
import os
import queue
import sys
import threading
import time
import traceback
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Any, Dict, Mapping, Optional

# ── Chemin vers le core ──────────────────────────────────────────────────────
APP_DIR = os.path.dirname(os.path.abspath(__file__))
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

try:
    from leia_living_core import LeiaLivingCore
except Exception as exc:
    LeiaLivingCore = None
    IMPORT_ERROR = exc
else:
    IMPORT_ERROR = None

# ══════════════════════════════════════════════════════════════════════════════
# PALETTE DE COULEURS
# ══════════════════════════════════════════════════════════════════════════════
BG          = "#0a0e17"       # fond principal très sombre
BG2         = "#0f1420"       # fond secondaire
PANEL       = "#131929"       # panneaux
PANEL2      = "#1a2235"       # panneaux clairs
BORDER      = "#1e2d45"       # bordures subtiles
BORDER2     = "#243450"       # bordures hover

TEXT        = "#e2e8f8"       # texte principal
TEXT2       = "#8899bb"       # texte secondaire
TEXT3       = "#4a5880"       # texte discret

ACCENT      = "#4f8ef7"       # bleu principal
ACCENT2     = "#6ba3ff"       # bleu clair
ACCENT_DIM  = "#1e3a6e"       # bleu foncé

LEIA_COLOR  = "#a78bfa"       # violet Leia
LEIA_DIM    = "#3b2f6e"       # violet foncé
USER_COLOR  = "#38bdf8"       # bleu utilisateur
USER_DIM    = "#0c3a5e"       # bleu utilisateur foncé

OK          = "#34d399"       # vert succès
OK_DIM      = "#0d3d2a"
WARN        = "#fbbf24"       # orange avertissement
WARN_DIM    = "#3d2e0a"
ERR         = "#f87171"       # rouge erreur
ERR_DIM     = "#3d1010"

BAR_BG      = "#0d1828"       # fond barres
BAR_LEIA    = "#7c3aed"       # barre Leia
BAR_HIGH    = "#f59e0b"       # barre tension/alerte

SYS_COLOR   = "#64748b"       # messages système

FONT_MAIN   = ("Segoe UI", 10)
FONT_TITLE  = ("Segoe UI", 13, "bold")
FONT_LARGE  = ("Segoe UI", 22, "bold")
FONT_MONO   = ("Consolas", 9)
FONT_CHAT   = ("Segoe UI", 11)
FONT_SMALL  = ("Segoe UI", 9)
FONT_LABEL  = ("Segoe UI", 9)


# ══════════════════════════════════════════════════════════════════════════════
# UTILITAIRES
# ══════════════════════════════════════════════════════════════════════════════

def clamp01(value: Any, default: float = 0.0) -> float:
    try:
        v = float(value)
    except Exception:
        v = default
    return max(0.0, min(1.0, v))


def safe_json(data: Any, max_chars: int = 14000) -> str:
    try:
        text = json.dumps(data, ensure_ascii=False, indent=2, default=str)
    except Exception:
        text = repr(data)
    if len(text) > max_chars:
        return text[:max_chars] + "\n… [tronqué]"
    return text


def deep_get(data: Mapping[str, Any], path: str, default: Any = None) -> Any:
    cur: Any = data
    for part in path.split("."):
        if isinstance(cur, Mapping):
            cur = cur.get(part, default)
        else:
            return default
    return cur


def format_time() -> str:
    return time.strftime("%H:%M:%S")


# ══════════════════════════════════════════════════════════════════════════════
# WIDGETS PERSONNALISÉS
# ══════════════════════════════════════════════════════════════════════════════

class ModernScrollText(tk.Frame):
    """Zone de texte avec scrollbar élégante."""

    def __init__(self, master, *, height=10, wrap="word", font=None, bg=None, fg=None):
        super().__init__(master, bg=bg or PANEL, bd=0, highlightthickness=0)
        _bg = bg or PANEL2
        _fg = fg or TEXT
        _font = font or FONT_MAIN

        self.text = tk.Text(
            self,
            bg=_bg, fg=_fg,
            insertbackground=ACCENT2,
            relief="flat", bd=0,
            padx=14, pady=10,
            height=height,
            wrap=wrap,
            font=_font,
            selectbackground=ACCENT_DIM,
            selectforeground=TEXT,
            spacing1=3, spacing3=3,
            cursor="arrow",
        )
        self.scroll = tk.Scrollbar(
            self, orient="vertical",
            command=self.text.yview,
            bg=PANEL, troughcolor=PANEL,
            activebackground=BORDER2,
            relief="flat", bd=0, width=6,
        )
        self.text.configure(yscrollcommand=self.scroll.set)
        self.text.pack(side="left", fill="both", expand=True)
        self.scroll.pack(side="right", fill="y")

    def set(self, value: str) -> None:
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("end", value)
        self.text.configure(state="disabled")

    def append(self, value: str, tag: Optional[str] = None) -> None:
        self.text.configure(state="normal")
        if tag:
            self.text.insert("end", value, tag)
        else:
            self.text.insert("end", value)
        self.text.see("end")
        self.text.configure(state="disabled")

    def clear(self) -> None:
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")


class GlowBar(tk.Frame):
    """Barre de métrique avec label, valeur numérique et canvas animé."""

    def __init__(self, master, label: str, color: str = BAR_LEIA):
        super().__init__(master, bg=PANEL, bd=0, highlightthickness=0)
        self._color = color
        self._value = 0.0

        # Label
        tk.Label(
            self, text=label,
            bg=PANEL, fg=TEXT2,
            font=FONT_LABEL, anchor="w", width=20,
        ).pack(side="left", padx=(0, 8))

        # Canvas barre
        self._canvas = tk.Canvas(
            self, height=8, bg=BAR_BG,
            bd=0, highlightthickness=0,
        )
        self._canvas.pack(side="left", fill="x", expand=True)

        # Valeur numérique
        self._val_label = tk.Label(
            self, text="0.00",
            bg=PANEL, fg=TEXT3,
            font=FONT_LABEL, width=5, anchor="e",
        )
        self._val_label.pack(side="left", padx=(6, 0))

        self.bind("<Configure>", self._redraw)

    def set_value(self, value: Any) -> None:
        self._value = clamp01(value, 0.0)
        self._val_label.configure(
            text=f"{self._value:.2f}",
            fg=self._pick_color(),
        )
        self._redraw()

    def _pick_color(self) -> str:
        if self._value > 0.75:
            return ERR
        if self._value > 0.5:
            return WARN
        return self._color

    def _redraw(self, event=None) -> None:
        w = self._canvas.winfo_width()
        h = self._canvas.winfo_height() or 8
        if w < 2:
            return
        self._canvas.delete("all")
        # Fond
        self._canvas.create_rectangle(0, 0, w, h, fill=BAR_BG, outline="")
        # Barre remplie
        filled = int(w * self._value)
        if filled > 0:
            col = self._pick_color()
            self._canvas.create_rectangle(0, 0, filled, h, fill=col, outline="")
            # Reflet lumineux
            if filled > 4:
                self._canvas.create_rectangle(
                    0, 0, filled, h // 3,
                    fill=self._lighten(col), outline="",
                )

    @staticmethod
    def _lighten(hex_color: str) -> str:
        try:
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            r = min(255, r + 60)
            g = min(255, g + 60)
            b = min(255, b + 60)
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            return hex_color


class StatusDot(tk.Canvas):
    """Petit indicateur rond coloré."""

    def __init__(self, master, size=10):
        super().__init__(
            master, width=size, height=size,
            bg=BG, bd=0, highlightthickness=0,
        )
        self._size = size
        self._color = TEXT3
        self._draw()

    def set_color(self, color: str) -> None:
        self._color = color
        self._draw()

    def _draw(self) -> None:
        s = self._size
        self.delete("all")
        self.create_oval(1, 1, s - 1, s - 1, fill=self._color, outline="")


class ModernButton(tk.Frame):
    """Bouton stylisé avec hover effect."""

    def __init__(self, master, text, command=None, icon="", width=None,
                 bg=PANEL2, fg=TEXT, hover_bg=BORDER2, accent=False):
        super().__init__(master, bg=bg, bd=0, highlightthickness=1,
                         highlightbackground=BORDER, cursor="hand2")
        self._bg = ACCENT_DIM if accent else bg
        self._hover_bg = ACCENT if accent else hover_bg
        self._fg = ACCENT2 if accent else fg
        self._command = command

        self.configure(bg=self._bg, highlightbackground=ACCENT_DIM if accent else BORDER)

        inner = tk.Frame(self, bg=self._bg)
        inner.pack(fill="both", expand=True, padx=10, pady=6)

        full_text = f"{icon}  {text}" if icon else text
        self._label = tk.Label(
            inner, text=full_text,
            bg=self._bg, fg=self._fg,
            font=FONT_SMALL, cursor="hand2",
        )
        if width:
            self._label.configure(width=width)
        self._label.pack()

        for w in (self, inner, self._label):
            w.bind("<Button-1>", self._on_click)
            w.bind("<Enter>", self._on_enter)
            w.bind("<Leave>", self._on_leave)

    def _on_click(self, e=None):
        if self._command:
            self._command()

    def _on_enter(self, e=None):
        self.configure(bg=self._hover_bg, highlightbackground=self._hover_bg)
        for w in self.winfo_children():
            try:
                w.configure(bg=self._hover_bg)
                for ww in w.winfo_children():
                    ww.configure(bg=self._hover_bg)
            except Exception:
                pass

    def _on_leave(self, e=None):
        self.configure(bg=self._bg, highlightbackground=ACCENT_DIM if self._hover_bg == ACCENT else BORDER)
        for w in self.winfo_children():
            try:
                w.configure(bg=self._bg)
                for ww in w.winfo_children():
                    ww.configure(bg=self._bg)
            except Exception:
                pass


class SectionTitle(tk.Frame):
    """Titre de section avec ligne décorative."""

    def __init__(self, master, text, icon=""):
        super().__init__(master, bg=PANEL, bd=0)
        row = tk.Frame(self, bg=PANEL)
        row.pack(fill="x", pady=(14, 6))

        if icon:
            tk.Label(row, text=icon, bg=PANEL, fg=ACCENT, font=("Segoe UI", 11)).pack(side="left", padx=(12, 6))

        tk.Label(
            row, text=text.upper(),
            bg=PANEL, fg=TEXT2,
            font=("Segoe UI", 8, "bold")
        ).pack(side="left")

        # Ligne décorative
        line = tk.Frame(self, bg=BORDER, height=1)
        line.pack(fill="x", padx=12)


# ══════════════════════════════════════════════════════════════════════════════
# INTERFACE PRINCIPALE
# ══════════════════════════════════════════════════════════════════════════════

class LeiaCompleteInterface(tk.Tk):

    def __init__(self) -> None:
        super().__init__()
        self.title("Leia  ·  Intelligence Vivante  ·  V19")
        self.geometry("1500x900")
        self.minsize(1100, 700)
        self.configure(bg=BG)

        # État interne
        self.tasks: "queue.Queue[tuple[str, Any]]" = queue.Queue()
        self.core: Optional[Any] = None
        self.last_snapshot: Dict[str, Any] = {}
        self.idle_enabled = tk.BooleanVar(value=False)
        self.auto_refresh = tk.BooleanVar(value=True)
        self.busy = False
        self._stop = False
        self._msg_count = 0

        self._setup_style()
        self._build_ui()
        self.after(100, self._bootstrap_core)
        self.after(120, self._drain_tasks)
        self.after(1200, self._periodic_refresh)

    # ── Style ttk ────────────────────────────────────────────────────────────

    def _setup_style(self) -> None:
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=TEXT)
        style.configure("TNotebook", background=PANEL, borderwidth=0, tabmargins=0)
        style.configure(
            "TNotebook.Tab",
            background=PANEL, foreground=TEXT3,
            padding=(16, 8),
            font=("Segoe UI", 9),
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", BG2)],
            foreground=[("selected", ACCENT2)],
        )
        style.configure(
            "Horizontal.TProgressbar",
            troughcolor=BAR_BG,
            background=BAR_LEIA,
            bordercolor=PANEL,
            lightcolor=BAR_LEIA,
            darkcolor=BAR_LEIA,
        )

    # ── Construction UI ───────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        # ── Barre supérieure ──────────────────────────────────────────────
        self._build_topbar()

        # ── Corps principal (3 colonnes) ──────────────────────────────────
        body = tk.PanedWindow(
            self, orient="horizontal",
            bg=BG, sashwidth=4,
            sashrelief="flat", sashpad=0,
        )
        body.pack(fill="both", expand=True, padx=0, pady=0)

        left   = tk.Frame(body, bg=PANEL, bd=0)
        center = tk.Frame(body, bg=BG2, bd=0)
        right  = tk.Frame(body, bg=PANEL, bd=0)

        body.add(left,   minsize=240, width=280)
        body.add(center, minsize=500, width=720)
        body.add(right,  minsize=280, width=500)

        self._build_left(left)
        self._build_center(center)
        self._build_right(right)

    # ── Barre supérieure ─────────────────────────────────────────────────────

    def _build_topbar(self) -> None:
        bar = tk.Frame(self, bg=BG, bd=0, height=54)
        bar.pack(fill="x", side="top")
        bar.pack_propagate(False)

        # Séparateur bas
        tk.Frame(bar, bg=BORDER, height=1).pack(side="bottom", fill="x")

        # Logo / Nom
        left_part = tk.Frame(bar, bg=BG)
        left_part.pack(side="left", padx=18, fill="y")

        tk.Label(
            left_part, text="⬡",
            bg=BG, fg=LEIA_COLOR,
            font=("Segoe UI", 20),
        ).pack(side="left", pady=8, padx=(0, 8))

        name_frame = tk.Frame(left_part, bg=BG)
        name_frame.pack(side="left", fill="y", pady=10)

        tk.Label(
            name_frame, text="LEIA",
            bg=BG, fg=TEXT,
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w")

        tk.Label(
            name_frame, text="Intelligence Vivante  ·  V19",
            bg=BG, fg=TEXT3,
            font=FONT_SMALL,
        ).pack(anchor="w")

        # Statut à droite
        right_part = tk.Frame(bar, bg=BG)
        right_part.pack(side="right", padx=18, fill="y")

        self._status_dot = StatusDot(right_part, size=10)
        self._status_dot.pack(side="left", pady=20, padx=(0, 8))

        self._status_label = tk.Label(
            right_part, text="Initialisation…",
            bg=BG, fg=TEXT3,
            font=FONT_SMALL,
        )
        self._status_label.pack(side="left", pady=20)

        # Séparateur central
        tk.Frame(bar, bg=BORDER, width=1).pack(side="right", fill="y", pady=10, padx=20)

        # Heure
        self._clock_label = tk.Label(
            bar, text=format_time(),
            bg=BG, fg=TEXT3, font=FONT_MONO,
        )
        self._clock_label.pack(side="right", padx=12, pady=16)
        self._tick_clock()

    def _tick_clock(self) -> None:
        self._clock_label.configure(text=format_time())
        self.after(1000, self._tick_clock)

    # ── Panneau gauche : état vivant + contrôles ──────────────────────────────

    def _build_left(self, parent: tk.Frame) -> None:
        # Scrollable
        canvas = tk.Canvas(parent, bg=PANEL, bd=0, highlightthickness=0)
        sb = tk.Scrollbar(parent, orient="vertical", command=canvas.yview,
                          bg=PANEL, troughcolor=PANEL, width=5, relief="flat")
        canvas.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        inner = tk.Frame(canvas, bg=PANEL)
        win_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        def _resize(e):
            canvas.configure(scrollregion=canvas.bbox("all"))
            canvas.itemconfig(win_id, width=e.width)

        inner.bind("<Configure>", _resize)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win_id, width=e.width))

        def _scroll(e):
            canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _scroll)

        # ── Section : État émotionnel ──────────────────────────────────
        SectionTitle(inner, "État Vivant", "◉").pack(fill="x")

        self.metrics: Dict[str, GlowBar] = {}
        metrics_def = [
            ("confidence",                    "Confiance",        BAR_LEIA),
            ("meta_risk",                     "Risque méta",      BAR_HIGH),
            ("emotional_state.tension",       "Tension",          ERR),
            ("emotional_state.resonance",     "Résonance",        OK),
            ("emotional_state.curiosity",     "Curiosité",        ACCENT),
            ("emotional_state.emotional_safety", "Sécurité",      OK),
            ("internal_needs.expression",     "Besoin d'exprimer",LEIA_COLOR),
            ("internal_needs.curiosity",      "Besoin comprendre",ACCENT2),
        ]
        for key, label, color in metrics_def:
            bar = GlowBar(inner, label, color)
            bar.pack(fill="x", padx=12, pady=3)
            self.metrics[key] = bar

        # ── Section : Dernière réponse ─────────────────────────────────
        SectionTitle(inner, "Dernière Réponse", "◎").pack(fill="x")

        resp_frame = tk.Frame(inner, bg=LEIA_DIM, bd=0,
                              highlightthickness=1, highlightbackground=LEIA_COLOR)
        resp_frame.pack(fill="x", padx=12, pady=(0, 4))

        self.last_response_box = tk.Text(
            resp_frame, bg=LEIA_DIM, fg=LEIA_COLOR,
            font=("Segoe UI", 10, "italic"),
            wrap="word", height=5, bd=0, padx=10, pady=8,
            relief="flat", state="disabled",
            cursor="arrow",
        )
        self.last_response_box.pack(fill="both")

        # ── Section : Contrôles ────────────────────────────────────────
        SectionTitle(inner, "Contrôles", "⚙").pack(fill="x")

        btns = tk.Frame(inner, bg=PANEL)
        btns.pack(fill="x", padx=12, pady=4)

        btn_defs = [
            ("Self-Test",        "⟳", self.run_self_test),
            ("Snapshot",         "◈", self.refresh_snapshot),
            ("Parole autonome",  "◆", lambda: self.autonomous_speak(force=False)),
            ("Forcer autonomie", "◉", lambda: self.autonomous_speak(force=True)),
            ("Donner un PDF",    "📄", self.load_pdf_book),
            ("Exporter JSON",    "↓", self.export_snapshot),
        ]
        for label, icon, cmd in btn_defs:
            ModernButton(btns, label, command=cmd, icon=icon).pack(
                fill="x", pady=2,
            )

        # ── Toggles ────────────────────────────────────────────────────
        SectionTitle(inner, "Options", "◈").pack(fill="x")

        opts = tk.Frame(inner, bg=PANEL)
        opts.pack(fill="x", padx=12, pady=(4, 16))

        def make_toggle(parent, text, var, cmd=None):
            f = tk.Frame(parent, bg=PANEL2, bd=0,
                         highlightthickness=1, highlightbackground=BORDER)
            f.pack(fill="x", pady=2)
            tk.Checkbutton(
                f, text=text, variable=var, command=cmd,
                bg=PANEL2, fg=TEXT2,
                selectcolor=ACCENT_DIM,
                activebackground=PANEL2,
                activeforeground=TEXT,
                font=FONT_SMALL,
                cursor="hand2",
            ).pack(anchor="w", padx=10, pady=6)

        make_toggle(opts, "  Idle vivant", self.idle_enabled, self.toggle_idle)
        make_toggle(opts, "  Rafraîchissement auto", self.auto_refresh)

    # ── Panneau central : chat ────────────────────────────────────────────────

    def _build_center(self, parent: tk.Frame) -> None:
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

        # ── Zone de chat ───────────────────────────────────────────────
        chat_outer = tk.Frame(parent, bg=BG2)
        chat_outer.pack(fill="both", expand=True)

        # En-tête chat
        chat_header = tk.Frame(chat_outer, bg=BG2, height=44)
        chat_header.pack(fill="x")
        chat_header.pack_propagate(False)

        tk.Label(
            chat_header, text="Dialogue",
            bg=BG2, fg=TEXT2,
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left", padx=16, pady=12)

        # Bouton effacer
        def _clear_chat():
            self.chat.clear()
            self._msg_count = 0

        ModernButton(
            chat_header, "Effacer", command=_clear_chat, icon="✕",
        ).pack(side="right", padx=10, pady=6)

        tk.Frame(chat_outer, bg=BORDER, height=1).pack(fill="x")

        # Zone messages
        self.chat = ModernScrollText(
            chat_outer, height=22,
            font=FONT_CHAT, bg=BG2, fg=TEXT,
        )
        self.chat.pack(fill="both", expand=True)

        # Tags de couleur
        self.chat.text.tag_configure(
            "user_name", foreground=USER_COLOR,
            font=("Segoe UI", 10, "bold"),
        )
        self.chat.text.tag_configure(
            "user_bubble", foreground=TEXT,
            lmargin1=20, lmargin2=20,
        )
        self.chat.text.tag_configure(
            "leia_name", foreground=LEIA_COLOR,
            font=("Segoe UI", 10, "bold"),
        )
        self.chat.text.tag_configure(
            "leia_bubble", foreground=TEXT,
            lmargin1=20, lmargin2=20,
        )
        self.chat.text.tag_configure(
            "system", foreground=SYS_COLOR,
            font=FONT_MONO,
            lmargin1=10, lmargin2=10,
        )
        self.chat.text.tag_configure(
            "time", foreground=TEXT3,
            font=("Segoe UI", 8),
        )
        self.chat.text.tag_configure(
            "divider", foreground=BORDER2,
        )

        # ── Zone de saisie ─────────────────────────────────────────────
        tk.Frame(chat_outer, bg=BORDER, height=1).pack(fill="x")

        input_area = tk.Frame(chat_outer, bg=PANEL, bd=0)
        input_area.pack(fill="x")

        input_inner = tk.Frame(input_area, bg=PANEL2, bd=0,
                               highlightthickness=1, highlightbackground=BORDER)
        input_inner.pack(fill="x", padx=14, pady=12)

        self.input_var = tk.StringVar()
        self.entry = tk.Entry(
            input_inner,
            textvariable=self.input_var,
            bg=PANEL2, fg=TEXT,
            insertbackground=ACCENT2,
            relief="flat", bd=0,
            font=("Segoe UI", 12),
        )
        self.entry.pack(side="left", fill="x", expand=True, ipady=11, padx=12)
        self.entry.bind("<Return>", lambda _e: self.send_message())

        # Focus highlight
        def _focus_in(e):
            input_inner.configure(highlightbackground=ACCENT)

        def _focus_out(e):
            input_inner.configure(highlightbackground=BORDER)

        self.entry.bind("<FocusIn>", _focus_in)
        self.entry.bind("<FocusOut>", _focus_out)

        send_btn = tk.Frame(
            input_inner, bg=ACCENT_DIM, bd=0,
            cursor="hand2",
            highlightthickness=1, highlightbackground=ACCENT,
        )
        send_btn.pack(side="right", padx=(0, 4), pady=4)

        send_label = tk.Label(
            send_btn, text="  Envoyer  ↵  ",
            bg=ACCENT_DIM, fg=ACCENT2,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )
        send_label.pack(padx=4, pady=6)

        def _send_hover(e):
            send_btn.configure(bg=ACCENT)
            send_label.configure(bg=ACCENT, fg=BG)

        def _send_leave(e):
            send_btn.configure(bg=ACCENT_DIM)
            send_label.configure(bg=ACCENT_DIM, fg=ACCENT2)

        for w in (send_btn, send_label):
            w.bind("<Button-1>", lambda e: self.send_message())
            w.bind("<Enter>", _send_hover)
            w.bind("<Leave>", _send_leave)

        # ── Terminal système ───────────────────────────────────────────
        tk.Frame(chat_outer, bg=BORDER, height=1).pack(fill="x")

        log_header = tk.Frame(chat_outer, bg=PANEL, height=32)
        log_header.pack(fill="x")
        log_header.pack_propagate(False)

        tk.Label(
            log_header, text="TERMINAL",
            bg=PANEL, fg=TEXT3,
            font=("Segoe UI", 8, "bold"),
        ).pack(side="left", padx=14, pady=8)

        self.log = ModernScrollText(
            chat_outer, height=6, wrap="none",
            font=FONT_MONO, bg=PANEL, fg=SYS_COLOR,
        )
        self.log.pack(fill="x")

    # ── Panneau droit : inspection interne ────────────────────────────────────

    def _build_right(self, parent: tk.Frame) -> None:
        # En-tête
        header = tk.Frame(parent, bg=PANEL, height=44)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="Inspection Interne",
            bg=PANEL, fg=TEXT2,
            font=("Segoe UI", 9, "bold"),
        ).pack(side="left", padx=16, pady=12)

        tk.Frame(parent, bg=BORDER, height=1).pack(fill="x")

        # Tabs
        self.tabs = ttk.Notebook(parent)
        self.tabs.pack(fill="both", expand=True)

        tab_defs = [
            ("Résumé",     "summary"),
            ("Impulsions", "impulse"),
            ("Mémoire",    "memory"),
            ("JSON brut",  "raw"),
        ]

        self._tab_boxes: Dict[str, ModernScrollText] = {}
        for label, key in tab_defs:
            frame = tk.Frame(self.tabs, bg=BG2)
            box = ModernScrollText(
                frame, height=10,
                font=FONT_MONO, bg=BG2, fg=TEXT2,
            )
            box.pack(fill="both", expand=True)
            self.tabs.add(frame, text=f"  {label}  ")
            self._tab_boxes[key] = box

        # Styles JSON (colorisation basique)
        for key in self._tab_boxes:
            box = self._tab_boxes[key]
            box.text.tag_configure("key",    foreground=ACCENT2)
            box.text.tag_configure("val_str",foreground=OK)
            box.text.tag_configure("val_num",foreground=WARN)
            box.text.tag_configure("val_bool",foreground=LEIA_COLOR)

    # ══════════════════════════════════════════════════════════════════════════
    # BOOTSTRAP CORE
    # ══════════════════════════════════════════════════════════════════════════

    def _bootstrap_core(self) -> None:
        if IMPORT_ERROR is not None or LeiaLivingCore is None:
            self._set_status("Erreur import", ERR)
            self.log.append(
                "✗ Erreur import leia_living_core:\n"
                + "".join(traceback.format_exception_only(type(IMPORT_ERROR), IMPORT_ERROR))
                + "\n",
                "system",
            )
            messagebox.showerror("Import impossible", str(IMPORT_ERROR))
            return
        self._set_status("Chargement…", WARN)
        self.log.append("◌ Chargement du LeiaLivingCore…\n")
        threading.Thread(target=self._worker_bootstrap, daemon=True).start()

    def _worker_bootstrap(self) -> None:
        try:
            core = LeiaLivingCore(user_id="interface", auto_start_idle=False)
            self.tasks.put(("core_ready", core))
        except Exception as exc:
            self.tasks.put(("error", ("Échec initialisation core", exc, traceback.format_exc())))

    # ══════════════════════════════════════════════════════════════════════════
    # DRAIN TÂCHES
    # ══════════════════════════════════════════════════════════════════════════

    def _drain_tasks(self) -> None:
        try:
            while True:
                kind, payload = self.tasks.get_nowait()

                if kind == "core_ready":
                    self.core = payload
                    self._set_status("En ligne", OK)
                    self.log.append("✓ Core chargé. Interface prête.\n")
                    self._append_system_chat("Leia est prête.")
                    self.refresh_snapshot()

                elif kind == "response":
                    user_text, response, snapshot = payload
                    self.busy = False
                    self._set_status("En ligne", OK)
                    self._append_message("Leia", response or "[silence]", "leia")
                    self.last_snapshot = snapshot or self._safe_snapshot()
                    self._render_snapshot()

                elif kind == "autonomous":
                    text, snapshot = payload
                    self.busy = False
                    self._set_status("En ligne", OK)
                    if text:
                        self._append_message("Leia", text, "leia")
                    else:
                        self.log.append("◌ Autonomie : rien de mûr pour l'instant.\n")
                    self.last_snapshot = snapshot or self._safe_snapshot()
                    self._render_snapshot()

                elif kind == "snapshot":
                    self.last_snapshot = payload or {}
                    self._render_snapshot()

                elif kind == "pdf_progress":
                    self.log.append(f"  {payload}\n")
                    self._set_status(str(payload)[:60], WARN)

                elif kind == "pdf_loaded":
                    result, snapshot = payload
                    self.busy = False
                    ok = bool(isinstance(result, Mapping) and result.get("success"))
                    self._set_status("PDF lu ✓" if ok else "PDF erreur", OK if ok else ERR)
                    self.log.append("PDF:\n" + safe_json(result, 5000) + "\n")
                    self.last_snapshot = snapshot or self._safe_snapshot()
                    self._render_snapshot()

                elif kind == "self_test":
                    self.busy = False
                    ok = bool(payload.get("ok"))
                    self._set_status("Self-test ✓" if ok else "Self-test ✗", OK if ok else ERR)
                    self.log.append("Self-test:\n" + safe_json(payload, 4000) + "\n")
                    self.refresh_snapshot()

                elif kind == "error":
                    title, exc, tb = payload
                    self.busy = False
                    self._set_status("Erreur", ERR)
                    self.log.append(f"✗ {title}: {exc}\n{tb}\n")

        except queue.Empty:
            pass
        self.after(120, self._drain_tasks)

    # ══════════════════════════════════════════════════════════════════════════
    # CHAT
    # ══════════════════════════════════════════════════════════════════════════

    def _append_message(self, speaker: str, text: str, role: str) -> None:
        self._msg_count += 1
        t = format_time()

        self.chat.text.configure(state="normal")

        if role == "user":
            self.chat.text.insert("end", f"\n  {t}  ", "time")
            self.chat.text.insert("end", f"Vous\n", "user_name")
            self.chat.text.insert("end", f"  {text.strip()}\n", "user_bubble")

        elif role == "leia":
            self.chat.text.insert("end", f"\n  {t}  ", "time")
            self.chat.text.insert("end", "Leia\n", "leia_name")
            self.chat.text.insert("end", f"  {text.strip()}\n", "leia_bubble")
            # Mise à jour panneau "dernière réponse"
            self.last_response_box.configure(state="normal")
            self.last_response_box.delete("1.0", "end")
            self.last_response_box.insert("end", text.strip())
            self.last_response_box.configure(state="disabled")

        self.chat.text.see("end")
        self.chat.text.configure(state="disabled")

    def _append_system_chat(self, text: str) -> None:
        self.chat.text.configure(state="normal")
        self.chat.text.insert("end", f"\n  ─── {text} ───\n", "system")
        self.chat.text.see("end")
        self.chat.text.configure(state="disabled")

    def send_message(self) -> None:
        if self.core is None or self.busy:
            return
        user_text = self.input_var.get().strip()
        if not user_text:
            return
        self.input_var.set("")
        self._append_message("Vous", user_text, "user")
        self.busy = True
        self._set_status("Leia réfléchit…", WARN)
        threading.Thread(target=self._worker_respond, args=(user_text,), daemon=True).start()

    def _worker_respond(self, user_text: str) -> None:
        try:
            assert self.core is not None
            response = self.core.respond(user_text)
            snapshot = self._safe_snapshot_thread()
            self.tasks.put(("response", (user_text, response, snapshot)))
        except Exception as exc:
            self.tasks.put(("error", ("Erreur réponse", exc, traceback.format_exc())))

    # ══════════════════════════════════════════════════════════════════════════
    # ACTIONS
    # ══════════════════════════════════════════════════════════════════════════

    def autonomous_speak(self, force: bool = False) -> None:
        if self.core is None or self.busy:
            return
        self.busy = True
        self._set_status("Autonomie…", WARN)
        threading.Thread(target=self._worker_autonomous, args=(force,), daemon=True).start()

    def _worker_autonomous(self, force: bool) -> None:
        try:
            assert self.core is not None
            text = self.core.autonomous_speak_if_ready(force=force) if hasattr(self.core, "autonomous_speak_if_ready") else None
            snapshot = self._safe_snapshot_thread()
            self.tasks.put(("autonomous", (text, snapshot)))
        except Exception as exc:
            self.tasks.put(("error", ("Erreur parole autonome", exc, traceback.format_exc())))

    def run_self_test(self) -> None:
        if self.core is None or self.busy:
            return
        self.busy = True
        self._set_status("Self-test…", WARN)
        threading.Thread(target=self._worker_self_test, daemon=True).start()

    def _worker_self_test(self) -> None:
        try:
            assert self.core is not None
            result = self.core.self_test() if hasattr(self.core, "self_test") else {"ok": False, "errors": ["self_test absent"]}
            self.tasks.put(("self_test", result))
        except Exception as exc:
            self.tasks.put(("error", ("Erreur self-test", exc, traceback.format_exc())))

    def refresh_snapshot(self) -> None:
        if self.core is None:
            return
        try:
            self.last_snapshot = self._safe_snapshot()
            self._render_snapshot()
        except Exception as exc:
            self.log.append(f"Snapshot impossible: {exc}\n")

    def load_pdf_book(self) -> None:
        if self.core is None or self.busy:
            return
        path = filedialog.askopenfilename(
            title="Donner un livre PDF à Leia",
            filetypes=[("PDF", "*.pdf"), ("Tous les fichiers", "*")],
        )
        if not path:
            return
        self.busy = True
        self._set_status("Lecture PDF…", WARN)
        self.log.append(f"PDF: {path}\n")
        threading.Thread(target=self._worker_load_pdf, args=(path,), daemon=True).start()

    def _worker_load_pdf(self, path: str) -> None:
        def progress(message: str) -> None:
            self.tasks.put(("pdf_progress", message))

        try:
            assert self.core is not None
            if not hasattr(self.core, "load_pdf_book"):
                result = {"success": False, "error": "load_pdf_book absent"}
            else:
                result = self.core.load_pdf_book(path, progress_callback=progress, max_pages=None, start_page=1)
            snapshot = self._safe_snapshot_thread()
            self.tasks.put(("pdf_loaded", (result, snapshot)))
        except Exception as exc:
            self.tasks.put(("error", ("Erreur PDF", exc, traceback.format_exc())))

    def export_snapshot(self) -> None:
        snap = self.last_snapshot or self._safe_snapshot()
        path = filedialog.asksaveasfilename(
            title="Exporter l'état Leia",
            defaultextension=".json",
            initialfile="leia_state_snapshot.json",
            filetypes=[("JSON", "*.json"), ("Tous les fichiers", "*")],
        )
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(snap, f, ensure_ascii=False, indent=2, default=str)
            self.log.append(f"✓ Exporté: {path}\n")
        except Exception as exc:
            messagebox.showerror("Export impossible", str(exc))

    def toggle_idle(self) -> None:
        if self.core is None:
            return
        try:
            if self.idle_enabled.get():
                self.core.start_idle_cycle(4.0)
                self.log.append("◉ Idle vivant activé.\n")
            else:
                self.core.stop_idle_cycle()
                self.log.append("◌ Idle vivant arrêté.\n")
        except Exception as exc:
            self.log.append(f"Erreur idle: {exc}\n")

    # ══════════════════════════════════════════════════════════════════════════
    # SNAPSHOT / RENDER
    # ══════════════════════════════════════════════════════════════════════════

    def _safe_snapshot(self) -> Dict[str, Any]:
        if self.core is None:
            return {}
        try:
            return dict(self.core.snapshot())
        except Exception:
            try:
                return dict(self.core.get_state_snapshot())
            except Exception:
                return {}

    def _safe_snapshot_thread(self) -> Dict[str, Any]:
        return self._safe_snapshot()

    def _render_snapshot(self) -> None:
        snap = self.last_snapshot or {}

        # Barres de métrique
        for path, bar in self.metrics.items():
            val = deep_get(snap, path, 0.0) if "." in path else snap.get(path, 0.0)
            bar.set_value(val)

        # Onglet résumé
        self._tab_boxes["summary"].set(safe_json({
            "public_response":       snap.get("public_response"),
            "confidence":            snap.get("confidence"),
            "meta_risk":             snap.get("meta_risk"),
            "should_answer":         snap.get("should_answer"),
            "inhibition_level":      snap.get("inhibition_level"),
            "emotional_state":       snap.get("emotional_state"),
            "internal_needs":        snap.get("internal_needs"),
            "identity_state":        snap.get("identity_state"),
            "conversation_field":    snap.get("conversation_field"),
            "autonomous_speech_ready": snap.get("autonomous_speech_ready"),
        }, 9000))

        # Onglet impulsions
        self._tab_boxes["impulse"].set(safe_json({
            "impulse":           snap.get("impulse"),
            "initiative":        snap.get("initiative"),
            "expression_intent": snap.get("expression_intent"),
            "intention_map":     snap.get("intention_map"),
            "internal_tension":  snap.get("internal_tension"),
            "micro_reactions":   snap.get("micro_reactions"),
        }, 9000))

        # Onglet mémoire
        self._tab_boxes["memory"].set(safe_json({
            "causal_memory":       snap.get("causal_memory"),
            "affective_memory":    snap.get("affective_memory"),
            "emotional_knowledge": snap.get("emotional_knowledge"),
            "dialogue_knowledge":  snap.get("dialogue_knowledge"),
            "personal_narrative":  snap.get("personal_narrative"),
            "long_causal_arc":     snap.get("long_causal_arc"),
        }, 9000))

        # Onglet JSON brut
        self._tab_boxes["raw"].set(safe_json(snap, 22000))

    def _periodic_refresh(self) -> None:
        if not self._stop and self.core is not None and self.auto_refresh.get() and not self.busy:
            try:
                self.last_snapshot = self._safe_snapshot()
                self._render_snapshot()
            except Exception:
                pass
        self.after(1300, self._periodic_refresh)

    # ══════════════════════════════════════════════════════════════════════════
    # STATUT
    # ══════════════════════════════════════════════════════════════════════════

    def _set_status(self, text: str, color: str) -> None:
        self._status_label.configure(text=text, fg=color)
        self._status_dot.set_color(color)

    # ══════════════════════════════════════════════════════════════════════════
    # FERMETURE
    # ══════════════════════════════════════════════════════════════════════════

    def destroy(self) -> None:
        self._stop = True
        try:
            if self.core is not None and hasattr(self.core, "stop_idle_cycle"):
                self.core.stop_idle_cycle()
        except Exception:
            pass
        super().destroy()


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main() -> None:
    app = LeiaCompleteInterface()
    app.mainloop()


if __name__ == "__main__":
    main()
