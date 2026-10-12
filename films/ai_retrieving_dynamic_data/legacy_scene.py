""""AI - Retrieving dynamic data" — standalone film, TRON style, no speaker (legacy scene).

A video that explains itself: keywords only, continuous pace.
Business example: parking (car park occupancy, sensors, subscriptions).

Architecture shown:
  - the problem: the AI chip wired straight onto the raw data;
  - the MCP: a semantic layer between the AI and the data;
  - the Harness: code (versioned, tested) that compiles into a frame AROUND the
    chip. It receives the question, lets the chip produce a tool call, checks that
    tool call (scope, rights) before running it through the MCP, then checks the
    answer (format) and traces everything (audit log).

On-screen text is written in English; `FR` holds the French version (FILM_LANG=fr).

    studio act ai_retrieving_dynamic_data harness   # one act, 480p draft + loop page
    studio dev ai_retrieving_dynamic_data           # whole film, 480p draft
    studio final ai_retrieving_dynamic_data --validated
"""

import json
import os
from pathlib import Path

import numpy as np
from manim import *

from studio.kit import primitives as kit
from studio.kit.actors import Chip
from studio.kit.i18n import Translator, current_lang
from studio.kit.primitives import (BODY, CYAN, DIMC, GREEN, ICE, LABEL, MONO, ORANGE, RED, TITLE, flash_along, globe,
                                   icon_check, icon_doc, icon_format, icon_list, icon_lock, icon_log, icon_mail,
                                   icon_scope, icon_sheet, icon_tool_card, icon_user, neon, rack, rail, square_dot)

FW = config.frame_width
HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("FILM_OUT", HERE))  # where chapters.json / meta.json are written

# --- Language: FILM_LANG=en (default) or fr. On-screen text is written in English; FR holds the French. --
LANG = current_lang()
FR = {  # English source text → French
    "AI - Retrieving dynamic data": "IA - Récupérer des données dynamiques", "01 · THE AI": "01 · L'IA",
    "02 · OUR REALITY": "02 · NOTRE RÉALITÉ", "03 · THE PROBLEM": "03 · LE PROBLÈME",
    "04 · WHAT DOES OUR DATA MEAN?": "04 · QUE VEULENT DIRE NOS DONNÉES ?",
    "What does our data mean?": "Que veulent dire nos données ?",
    "05 · HARNESS → TRUST": "05 · HARNESS → LA CONFIANCE", "06 · TOGETHER": "06 · ENSEMBLE",
    "General AI": "L'IA générale", "Our reality": "Notre réalité", "The problem": "Le problème",
    "Harness: trust": "Harness : la confiance", "Together": "Ensemble", "AI": "IA", "BOOKS": "LIVRES",
    "PUBLIC DATA": "DONNÉES PUBLIQUES", "WRITE A CLIENT EMAIL": "RÉDIGE UN MAIL CLIENT", "EMAIL READY": "E-MAIL PRÊT",
    "SUMMARISE A CONTRACT": "RÉSUME UN CONTRAT", "5 KEY POINTS": "5 POINTS CLÉS",
    "WRITE AN EXCEL FORMULA": "ÉCRIS UNE FORMULE EXCEL", "FORMULA": "FORMULE", "GENERAL AI": "IA GÉNÉRALE",
    "FAST · VERSATILE": "RAPIDE · POLYVALENTE", "OUR CAR PARKS · PARIS?": "NOS PARKINGS · PARIS ?",
    "MEMORY": "MÉMOIRE", "SOURCE: WEB": "SOURCE : WEB", "WORLD": "MONDE", "TENS": "DES DIZAINES",
    "HUNDREDS": "DES CENTAINES", "THOUSANDS": "DES MILLIERS", "OF CAR PARKS": "DE PARKINGS",
    "MILLIONS": "DES MILLIONS", "TENS OF MILLIONS": "DES DIZAINES DE MILLIONS",
    "OF EVENTS / DAY": "D'ÉVÉNEMENTS / JOUR", "TERABYTES": "DES To", "HUNDREDS OF TB": "DES CENTAINES DE To",
    "PETABYTES": "DES Po", "STORED": "STOCKÉS", "DATABASES": "BASES DE DONNÉES", "SENSORS": "CAPTEURS",
    "TICKETING": "BILLETTERIE", "SUBSCRIPTIONS": "ABONNEMENTS", "MASTER DATA": "RÉFÉRENTIEL",
    "DOZENS OF SYSTEMS · HUNDREDS OF TABLES": "DES DIZAINES DE SYSTÈMES · DES CENTAINES DE TABLES",
    "PRIVATE": "PRIVÉ", "PARKING SESSIONS · PARIS · SEPT.?": "STATIONNEMENTS · PARIS · SEPT. ?",
    "DIRECT ACCESS TO TABLES": "ACCÈS DIRECT AUX TABLES", "AMBIGUOUS": "AMBIGUË",
    "4 DEFINITIONS → 4 ANSWERS": "4 DÉFINITIONS → 4 RÉPONSES", "CAR PARKS": "PARKINGS", "+ STREET": "+ VOIRIE",
    "NO DUPLICATES": "SANS DOUBLONS", "WITH DUPLICATES": "AVEC DOUBLONS", "1.12 M": "1,12 M", "1.48 M": "1,48 M",
    "1.86 M": "1,86 M", "2.41 M": "2,41 M", "SEMANTIC LAYER": "COUCHE SÉMANTIQUE", "TOOL CALL": "APPEL D'OUTIL",
    "TABLES": "TABLEAUX", "CHARTS": "GRAPHIQUES", "REPORTS": "RAPPORTS",
    "UNDERSTAND THE DATA BETTER": "MIEUX COMPRENDRE LES DONNÉES",
    "RETRIEVING DYNAMIC DATA": "RÉCUPÉRER DES DONNÉES DYNAMIQUES", "UNDERSTANDING": "COMPRÉHENSION",
    "DATA": "DONNÉES", "DIRECTOR": "DIRECTEUR", "USER": "UTILISATEUR",
    "PARKING SESSIONS · SEPT.?": "STATIONNEMENTS · SEPT. ?", "WEST ZONE": "ZONE OUEST", "0.31 M": "0,31 M",
    "OFF-STREET · WEST ZONE · 09/26": "HORS VOIRIE · ZONE OUEST · 09/26",
    "09:14 sessions · west OK": "09:14 sessions · ouest OK", "TOOLS": "OUTILS", "0.74 M": "0,74 M",
    "DEFAULT · CAR PARKS": "PAR DÉFAUT · PARKINGS", "NO MAP": "SANS CARTE", "DIRECT QUERY": "REQUÊTE DIRECTE",
    "SENT TO MCP": "ENVOYÉ AU MCP", "TRUST": "CONFIANCE",
    "WHAT DOES OUR DATA MEAN?": "QUE VEULENT DIRE NOS DONNÉES ?", "PARKING SESSIONS": "STATIONNEMENTS",
    "ON-STREET SESSIONS": "SESSIONS VOIRIE", "OFF-STREET SESSIONS": "SESSIONS HORS VOIRIE",
    "CAR PARKS · NO DUPLICATES": "PARKINGS · SANS DOUBLONS",
    "CAR PARKS · NO DUPLICATES · 09/26": "PARKINGS · SANS DOUBLONS · 09/26", "occupancy()": "occupation()",
    "capacity()": "capacite()", "contracts()": "contrats()", "customers()": "clients()", "scope()": "perimetre()",
    "pricing()": "tarifs()", "SCOPE": "PÉRIMÈTRE", "RIGHTS": "DROITS", "audit.log": "journal.log",
}


tr = Translator(FR, LANG)


def L(text, *a, **k):
    return kit.label(tr(text), *a, **k)


def T_(text, **k):
    """Translated Text()."""
    return Text(tr(text), **k)


# --- Business example (illustrative figures, to be replaced by real ones) -----------------------------
QUESTION = tr("PARKING SESSIONS · PARIS · SEPT.?")
CALL_OK = tr('stationnements("PARIS", "09/26")')
# tree of possibilities: 2 definitions × 2 ways of counting = 4 answers
TREE_L1 = [tr(x) for x in ["CAR PARKS", "+ STREET"]]
TREE_L2 = [tr(x) for x in ["NO DUPLICATES", "WITH DUPLICATES"]]
TREE_LEAVES = [tr(x) for x in ["1.12 M", "1.48 M", "1.86 M", "2.41 M"]]   # (P,no dup) (P,dup) (P+S,no dup) (P+S,dup)
TRIES = [1, 3]                                         # leaf picked at each attempt (never the right one)
GUESSES = [TREE_LEAVES[i] for i in TRIES]
GOOD = (tr("1.12 M"), tr("CAR PARKS · NO DUPLICATES · 09/26"))
QUESTION_ME = tr("PARKING SESSIONS · SEPT.?")            # no zone: the harness derives it from the user's rights
# the user's context grows act by act: 02 · 04 (with the MCP) · 05 (when SCOPE asks for it)
USER_CTX = [["INDIGO", "USER"], ["INDIGO", "DIRECTOR"], ["INDIGO", "DIRECTOR", "WEST ZONE"]]  # [1] unused
# Deliberately vague orders of magnitude (no precise figures until validated)
LEVELS = ["PARIS", "FRANCE", "WORLD"]
PARKS_MAG = ["TENS", "HUNDREDS", "THOUSANDS"]
EVENTS_MAG = ["THOUSANDS", "MILLIONS", "TENS OF MILLIONS"]
STORAGE_MAG = ["TERABYTES", "HUNDREDS OF TB", "PETABYTES"]
RACKS = [1, 5, 12]                         # databases lit per level
SYSTEMS = ["SENSORS", "TICKETING", "SUBSCRIPTIONS", "CRM", "FINANCE", "MASTER DATA"]
# deliberately confusing tables: duplicates, versions, temp tables, overlapping notions
TABLES = ["stn_evt_raw", "stn_evt_v2", "stn_v2_bkp", "stat_park_tmp", "pk_site_ref", "tkt_pass_24",
          "voirie_horod", "abo_ctr_24", "zone_idf_map", "cpt_old_2019"]
CONCEPTS = [("ON-STREET SESSIONS", 6), ("OFF-STREET SESSIONS", 0), ("CAR PARKS", 4), ("SUBSCRIPTIONS", 7), ("ZONES", 8)]
CONCEPT_TABLES = [[6], [0, 5], [4], [7], [8]]   # tables read by each MCP domain
TEXT_DIM = 0.6                                  # act 03: tree labels stay readable when dimmed
BOTTOM_DIM = 0.25                               # act 03: wiring and tree dimmed while the panel is shown
CHIP_IN_HARNESS = 0.8                           # chip scale once inside the harness
RUN_LINES = ["check_format(question)", "tools = mcp.list_tools()", "scope = user.zone()",
             "assert user.can_read(tool)", "data = mcp.call(tool, scope)", "log.trace(request)"]
GATE_LINE = {0: 0, 1: 2, 2: 3, 3: 5}               # harness module → line of harness.py that runs
TOOLS_H = 1.2                                  # height of the TOOLS step, above the chip
SEL = 1                                         # domain picked for the question (off-street = car parks)
# each domain exposes 2 tools, each tool reads one table (almost every valid table is wired)
TOOLS = [[("sessions()", 0), ("occupancy()", 5)], [("sites()", 4), ("capacity()", 6)],
         [("contracts()", 7), ("customers()", 7)], [("scope()", 8), ("pricing()", 6)]]
LEAF_TABLES = [[0], [0, 2], [1, 6], [3, 6, 9]]   # tables read by each definition (tree leaf)

# --- Diagram layout ------------------------------------------------------------------------------------
CHIP_POS = np.array([-1.2, 1.15, 0])
OUT_Y = 1.15
USER_POS = np.array([-6.55, OUT_Y, 0])
CHAT_C = np.array([-4.95, OUT_Y, 0])         # the chat window (the user) left of the chip
CHAT_W, CHAT_H = 3.4, 1.9
IN_X = CHAT_C[0] + CHAT_W / 2                # right edge of the chat: where questions leave
ANS_POS = np.array([5.55, OUT_Y, 0])
ANS_IN = ANS_POS + LEFT * 1.25
FRAME = (np.array([0.225, 0.575, 0]), 5.55, 3.65)          # the Harness surrounds the chip
GATES = [  # (name, icon, position, label side)  — in the order of the lines of harness.py
    ("FORMAT", icon_format, np.array([-2.55, OUT_Y, 0]), DOWN),   # on the way in, before the chip
    ("SCOPE", icon_scope, np.array([-1.2, -0.25, 0]), LEFT),
    ("RIGHTS", icon_lock, np.array([-1.2, -0.9, 0]), LEFT),
    ("TRACE", icon_log, np.array([1.6, OUT_Y, 0]), DOWN),
]
JOURNAL_C = np.array([1.85, OUT_Y, 0])   # the audit log lives in the harness, instead of the TRACE icon
BUS_Y = -1.3
BAND_Y = -2.05
DATA_Y = -3.35
TABLE_XS = list(np.linspace(-6.1, 6.1, 10))
J1_POS = [np.array([-3.6, -0.95, 0]), np.array([3.0, -0.95, 0])]   # branch CAR PARKS / + STREET
J2_DX, J2_Y = 1.3, -1.85                                            # branch NO / WITH DUPLICATES

# --- Map ------------------------------------------------------------------------------------------------
MAP_C = np.array([-18.0, 0.0, 0])
# Act 02 split screen: the map (built around MAP_C) is scaled down and placed below the boundary
SPLIT_Y = -0.02                                   # PUBLIC (top) / PRIVATE (bottom) boundary
TOP_Y = 2.45                                    # the boundary rises to here when our world unfolds
PV_K = 0.9                                      # scale of the private area
PV_REF = MAP_C + np.array([1.05, -0.075, 0])    # centre of the map content
PV_DEST = np.array([0.1, -0.85, 0])             # where that centre appears on screen
PUSH = dict(scale=0.45, to=np.array([-1.4, 3.25, 0]))  # the chip (and the user) pushed to the top
MC = MAP_C + UP * 0.3
COS = np.cos(np.radians(48))
FR_C, FR_K = (2.5, 46.6), 0.56
EU_C, EU_K = (10.0, 52.0), 0.19
FRANCE = [(2.5, 51.1), (4.2, 50.0), (8.2, 49.0), (7.5, 47.5), (6.8, 46.4), (7.6, 45.2), (7.0, 44.0), (7.5, 43.7),
          (4.8, 43.3), (3.1, 43.2), (3.2, 42.4), (1.5, 42.5), (-1.8, 43.4), (-1.2, 46.0), (-2.2, 47.2), (-4.7, 48.5),
          (-1.6, 48.7), (-1.5, 49.7), (0.2, 49.5), (1.6, 50.9), (2.5, 51.1)]
FR_CITIES = [(2.35, 48.85, 9), (4.85, 45.76, 4), (5.37, 43.3, 3), (3.06, 50.63, 3), (-0.58, 44.84, 3), (1.44, 43.6, 3),
             (-1.55, 47.2, 3), (7.75, 48.58, 2), (7.26, 43.7, 2), (-1.68, 48.11, 2), (3.88, 43.61, 2), (5.72, 45.19, 2)]
WORLD_DOTS = [(0.22, 0.55), (0.27, 0.5), (0.3, 0.58), (0.2, 0.47), (0.33, 0.52), (0.25, 0.6), (-0.55, 0.45),
              (-0.48, 0.38), (-0.62, 0.52), (-0.42, 0.5), (-0.3, -0.25), (-0.25, -0.38), (-0.33, -0.12), (0.62, 0.38),
              (0.7, 0.3)]


def ll(lon, lat, k, c, center=MC):
    return center + np.array([(lon - c[0]) * COS * k, (lat - c[1]) * k, 0])


TASK_ICONS = [icon_mail, icon_doc, icon_sheet]


class Film(MovingCameraScene):
    slow = 1.0        # slow-motion factor (introduction)
    MIN_RT = 0.5      # minimum animation duration (avoids abrupt pops)
    _raw = False      # True while packets move (exact durations)


    def construct(self):
        self.chapters = []
        self.chapter_lbl = None
        acts = [  # (name, slow-motion, scenes)
            ("ai", 1.0, [self.a1_general_ai]),
            ("reality", 1.0, [self.a2_our_data, self.a2_zoom_out]),
            ("problem", 1.0, [self.a3_direct_access, self.a3_random_guesses, self.a3_ambiguity]),
            ("mcp", 1.0, [self.a4_semantic_layer]),
            ("harness", 1.0, [self.a5_build_harness, self.a5_scoped_question, self.a5_condense]),
            ("together", 1.0, [self.a6_together]),
        ]
        # Partial drafts (studio act / range): earlier acts are computed but not drawn.
        names = [a[0] for a in acts]
        upto = os.environ.get("FILM_UPTO")  # FILM_UPTO=problem: stop after this act
        start = os.environ.get("FILM_FROM")  # FILM_FROM=problem: earlier acts are computed but not drawn
        for act in (upto, start):
            if act and act not in names:
                raise ValueError(f"Unknown act: {act} (acts: {', '.join(names)})")
        act_starts = {}
        for name, slow, scenes in acts:
            act_starts[name] = round(self.now(), 2)
            if start:
                self.next_section(name, skip_animations=names.index(name) < names.index(start))
            self.slow = slow
            for scene in scenes:
                scene()
            if upto == name:
                self.hold(0.8)
                break
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / "chapters.json").write_text(json.dumps(self.chapters, ensure_ascii=False, indent=1))
        (OUT / "meta.json").write_text(json.dumps({"lang": LANG, "title": tr("AI - Retrieving dynamic data"),
                                                   "acts": act_starts}, ensure_ascii=False))

    # --- Helpers -----------------------------------------------------------------------------------------
    def play(self, *anims, **kw):
        rt = kw.get("run_time")
        if rt is None:
            rt = max([a.run_time for a in anims if isinstance(a, Animation)] or [1.0])
        if not self._raw and 0.1 < rt < self.MIN_RT:  # jolts (< 0.1 s) and packets are exempt
            rt = self.MIN_RT
        kw["run_time"] = rt * self.slow
        super().play(*anims, **kw)

    def wait(self, duration=1.0, *args, **kw):
        super().wait(duration * self.slow, *args, **kw)

    def hold(self, t=0.6):
        self.wait(t)

    def morph(self, old, new, *extra, run_time=0.8):
        """What leaves turns into what arrives (3Blue1Brown-style morph), element by element:
        each old element is paired with a new one; extra elements fade out in place."""
        olds = [m for g in old for m in (g if isinstance(g, VGroup) and not hasattr(g, "text") and len(g) > 2
                                           and all(isinstance(x, VGroup) for x in g) else [g])]
        news = [m for g in new for m in (g if isinstance(g, VGroup) and not hasattr(g, "text") and len(g) > 2
                                           and all(isinstance(x, VGroup) for x in g) else [g])]
        anims, n = [], min(len(olds), len(news))
        for o, w in zip(olds[:n], news[:n]):
            anims.append(FadeTransform(o, w, path_arc=-PI / 12))
        anims += [FadeOut(o, scale=0.9) for o in olds[n:]] + [FadeIn(w, scale=0.9) for w in news[n:]]
        self.play(*anims, *extra, run_time=run_time, rate_func=rate_functions.ease_in_out_cubic)

    def now(self):
        return float(self.renderer.time)

    def packet(self, color=ICE):
        p = VGroup(Square(0.12).set_fill(color, 1).set_stroke(width=0),
                   Square(0.24).set_fill(color, 0.15).set_stroke(width=0))
        return p.set_z_index(8)

    def send(self, packet, points, color, run_time=1.0):
        path = rail(points)
        packet.move_to(points[0])
        trail = TracedPath(packet.get_center, stroke_color=color, stroke_width=3, dissipating_time=0.35)
        trail.set_z_index(7)
        self.add(trail, packet)
        self._raw = True
        self.play(MoveAlongPath(packet, path), run_time=run_time, rate_func=rate_functions.ease_in_out_sine)
        self._raw = False
        self.remove(trail)

    def dim(self, mobs, factor):
        """Dim (or restore, factor=1) a group while respecting each layer's own opacity."""
        fam = [m for mob in mobs for m in mob.family_members_with_points()]
        for m in fam:
            if not hasattr(m, "_base_op"):
                m._base_op = (m.get_stroke_opacity(), m.get_fill_opacity())
        start = [(m.get_stroke_opacity(), m.get_fill_opacity()) for m in fam]
        end = [(b[0] * factor, b[1] * factor) for b in (m._base_op for m in fam)]

        def update(_, a):
            for m, (s0, f0), (s1, f1) in zip(fam, start, end):
                m.set_stroke(opacity=s0 + (s1 - s0) * a, family=False)
                m.set_fill(opacity=f0 + (f1 - f0) * a, family=False)

        return UpdateFromAlphaFunc(Mobject(), update)

    def chapter(self, text, toc=None, src=None, extra=()):
        """Small chapter label, pinned top-left of the camera frame."""
        self.chapters.append([round(self.now(), 2), tr(toc or text)])
        frame = self.camera.frame
        new = L(text, 14, GREY_B, spacing=6).set_z_index(30)
        h0 = new.height

        def stick(m):
            s = frame.width / FW
            m.scale_to_fit_height(h0 * s)
            m.move_to(frame.get_corner(UL) + np.array([0.45, -0.4, 0]) * s, aligned_edge=UL)

        stick(new)
        new.add_updater(stick)
        if src is not None:  # an element of the scene rises and becomes the chapter title
            self.play(FadeOut(self.chapter_lbl, shift=LEFT * 0.1), FadeTransform(src, new), *extra, run_time=0.8)
        elif self.chapter_lbl is None:
            self.play(FadeIn(new, shift=RIGHT * 0.15), run_time=0.5)
        else:  # the old title fades before the new one appears
            self.play(LaggedStart(FadeOut(self.chapter_lbl, shift=LEFT * 0.1), FadeIn(new, shift=RIGHT * 0.15),
                                  lag_ratio=0.7), run_time=0.7)
        self.chapter_lbl = new


    PIN_SIDES = {"UP": 0, "DOWN": 1, "LEFT": 2, "RIGHT": 3}
    PIN_OPS = (0.03, 0.07, 0.16, 1.0)  # opacities of the 3 halos + core (see neon)

    def pin_parts(self, side, k):
        i = self.PIN_SIDES[side] * 5 + (k + 2)
        return [g[i] for g in self.chip.pins[0]] + [self.chip.pins[1][i]]

    def hide_pins(self):
        """Chip without pins: they only appear once connected."""
        self.pins_on = set()
        for side in self.PIN_SIDES:
            for k in range(-2, 3):
                for part in self.pin_parts(side, k):
                    part.set_stroke(opacity=0)

    def show_pins(self, *keys):
        """Animations: show the pins (side, k) that receive a connection."""
        anims = []
        for side, k in keys:
            if (side, k) in self.pins_on:
                continue
            self.pins_on.add((side, k))
            for part, op in zip(self.pin_parts(side, k), self.PIN_OPS):
                anims.append(part.animate.set_stroke(opacity=op))
        return anims

    def pin(self, k):
        """Tip of the k-th bottom pin of the chip (k = -2 … 2, 0 = centre)."""
        return self.chip.body.get_center() + np.array([-k * self.chip.size * 0.17, -(self.chip.size / 2 + 0.16), 0])

    def make_chat(self):
        win = RoundedRectangle(corner_radius=0.14, width=CHAT_W, height=CHAT_H).move_to(CHAT_C)
        head = Line(win.get_corner(UL) + DOWN * 0.38, win.get_corner(UR) + DOWN * 0.38).set_stroke(DIMC, 1)
        title = VGroup(Circle(0.05).set_fill(ORANGE, 1).set_stroke(width=0), L("CHAT · IA", 9, GREY_B, spacing=4))
        title.arrange(RIGHT, buff=0.12).move_to(win.get_corner(UL) + np.array([0.22, -0.19, 0]), aligned_edge=LEFT)
        self.chat_win = win
        self.q_box = None
        return VGroup(neon(win, ICE, 1.6, fill=BODY), head, title).set_z_index(3)

    def chat_bubble_pos(self):
        return self.chat_win.get_corner(UR) + np.array([-0.2, -0.62, 0])

    def doc_to_question(self, text):
        """The question is typed in the chat window (which stands for the user)."""
        txt = L(text, 10, ICE, spacing=2)
        box = RoundedRectangle(corner_radius=0.1, width=txt.width + 0.36, height=txt.height + 0.24)
        box.set_fill(ManimColor("#0B2730"), 1).set_stroke(width=0)
        bub = VGroup(box, txt.move_to(box)).move_to(self.chat_bubble_pos(), aligned_edge=UR).set_z_index(4)
        anims = [FadeIn(box, shift=LEFT * 0.1)]
        if self.q_box is not None:
            anims.append(FadeOut(self.q_box))
        self.play(*anims, run_time=0.3)
        self._raw = True
        self.play(AddTextLetterByLetter(txt, time_per_char=0.02), run_time=0.5)
        self._raw = False
        self.q_box = box
        return txt


    def q_label(self, text):
        """Question text placed in the chat bubble."""
        q = L(text, 10, ICE, spacing=2).set_z_index(4)
        if self.q_box is not None:
            return q.move_to(self.q_box)
        return q.move_to(self.chat_bubble_pos(), aligned_edge=UR)

    def ask(self, color=ICE, run_time=0.6):
        p = self.packet(color)
        self.send(p, [[IN_X, OUT_Y, 0], self.chip.port(LEFT)], color, run_time=run_time)
        self.play(self.chip.pulse(), FadeOut(p), run_time=0.45)

    # --- 01 · The AI: trained on the world, then general-purpose… but not on our data ---------------------------
    def a1_general_ai(self):
        self.chapter("01 · THE AI", "General AI")
        c = CHIP_POS
        sources = VGroup()
        for k, name in enumerate(["WEB", "BOOKS", "WIKIS", "CODE", "ARTICLES", "FORUMS"]):
            col, row = divmod(k, 3)  # two lists: 3 sources on the left, 3 on the right
            pos = np.array([-4.95 if col == 0 else 2.55, c[1] + 0.8 - 0.8 * row, 0])
            lbl = L(name, 12, CYAN, spacing=4)
            box = RoundedRectangle(corner_radius=0.06, width=lbl.width + 0.4, height=0.4).move_to(pos)
            sources.add(VGroup(neon(box, CYAN, 1.2, fill=BODY), lbl.move_to(box)))
        public = L("PUBLIC DATA", 13, CYAN, spacing=6).move_to(c + DOWN * 2.95)
        self.play(LaggedStart(*[FadeIn(s, scale=0.85) for s in sources], lag_ratio=0.15), FadeIn(public),
                  run_time=1.0)
        self.play(public.animate.set_opacity(0.3), run_time=0.3)  # dimmed until relevant

        # the streams converge… and the chip is born from this data
        rng = np.random.default_rng(1)


        # dissolve: each dot flies to a point of the chip outline, which appears where they land
        self.chip = Chip(label_text=tr("AI")).move_to(c)
        # circuit weaving: each source sends right-angle rails towards the chip;
        # on arrival the rails draw the outline, then the core, then the pins; the words slide
        # along their rail and melt into the chip
        chip = self.chip
        self.hide_pins()
        traces, words = VGroup(), []
        for k, src in enumerate(sources):
            col, row = divmod(k, 3)
            side = "LEFT" if col == 0 else "RIGHT"
            off = (1 - row) * 0.17 * chip.size
            end = chip.port(LEFT if col == 0 else RIGHT) + UP * off
            edge = src[0][1]
            start = edge.get_right() if col == 0 else edge.get_left()
            mid_x = (start[0] + end[0]) / 2 + (row - 1) * 0.12 * (1 if col == 0 else -1)
            traces.add(rail([start, [mid_x, start[1], 0], [mid_x, end[1], 0], end], CYAN, 1.6))
            words.append(src[1])
        pins_used = [(s_, k_) for s_ in ("LEFT", "RIGHT") for k_ in (-1, 0, 1)]
        # 1 · rails are drawn from the sources (the frames go dark)
        self.play(LaggedStart(*[Create(t) for t in traces], lag_ratio=0.03),
                  *[src[0].animate.set_stroke(opacity=0.25) for src in sources], run_time=1.0)
        # 2 · energy flows and draws the chip: outline → core → pins
        self.play(*[flash_along(t, WHITE, 4, run_time=1.0) for t in traces],
                  Create(chip.body), Create(chip.wires), public.animate.set_opacity(1), run_time=0.8)
        self.play(Create(chip.die), Create(chip.pins, lag_ratio=0.05), *self.show_pins(*pins_used), run_time=0.6)
        # 3 · the words slide along their rail and melt into the chip
        word_moves, ghosts = [], []
        for w in words:
            g = w.copy()
            ghosts.append(g)
            word_moves.append(g.animate(rate_func=rate_functions.ease_in_cubic).move_to(chip.get_center())
                              .scale(0.3).set_opacity(0))
        self.play(*word_moves, *[src[0].animate.set_stroke(opacity=0.6) for src in sources], FadeIn(chip.label),
                  traces.animate.set_stroke(DIMC), chip.pulse(CYAN), run_time=0.7)
        self.remove(*ghosts)
        self.remove(*chip.submobjects)
        self.add(chip)
        self.sources, self.traces = sources, traces
        self.hold(0.3)


        # a general intelligence: tasks and their results grow out of the chip, along rails
        tasks = [("WRITE A CLIENT EMAIL", "EMAIL READY"), ("SUMMARISE A CONTRACT", "5 KEY POINTS"),
                 ("WRITE AN EXCEL FORMULA", "FORMULA")]
        chip = self.chip
        ins, outs, branches = VGroup(), VGroup(), VGroup()
        self.play(public.animate.set_opacity(0.3), run_time=0.3)
        self.public = public  # "PUBLIC DATA" stays until act 2
        lefts, rights = VGroup(), VGroup()
        for k, (task, result) in enumerate(tasks):
            y = c[1] + 0.8 - 0.8 * k
            off = (1 - k) * 0.17 * chip.size
            box = RoundedRectangle(corner_radius=0.06, width=3.25, height=0.46).move_to([-4.95, y, 0])
            icon = TASK_ICONS[k](ICE).scale_to_fit_height(0.24).move_to(box.get_left() + RIGHT * 0.3)
            label = L(task, 11, ICE, spacing=3).move_to(box.get_center() + RIGHT * 0.2)
            ins.add(VGroup(neon(box, DIMC, 1.2, fill=BODY), label, icon))
            outs.add(VGroup(icon_check(GREEN, 0.55), L(result, 13, GREEN, spacing=3)).arrange(RIGHT, buff=0.15)
                     .move_to([2.3, y, 0], aligned_edge=LEFT).set_color(GREY_B))
            pl, pr = chip.port(LEFT) + UP * off, chip.port(RIGHT) + UP * off
            mx_l, mx_r = pl[0] - 0.35 - 0.12 * k, pr[0] + 0.35 + 0.12 * k
            lefts.add(rail([[box.get_right()[0], y, 0], [mx_l, y, 0], [mx_l, pl[1], 0], pl], DIMC, 1.6))
            rights.add(rail([pr, [mx_r, pr[1], 0], [mx_r, y, 0], [outs[-1].get_left()[0] - 0.12, y, 0]], DIMC, 1.6))
        branches.add(*lefts, *rights)
        # the whole circuit appears at once (tasks + rails); then each example runs through it very fast
        srcs, trs = self.sources, self.traces
        self.play(*[FadeTransform(srcs[k], ins[k]) for k in range(3)],
                  *[FadeTransform(srcs[3 + k], outs[k]) for k in range(3)],
                  *[ReplacementTransform(trs[k], lefts[k]) for k in range(3)],
                  *[ReplacementTransform(trs[3 + k], rights[k]) for k in range(3)],
                  run_time=0.9, rate_func=rate_functions.ease_in_out_cubic)
        self._raw = True
        for k in range(3):  # each example runs through the circuit: the rail and the result turn green (match)
            self.play(lefts[k].animate.set_stroke(GREEN), rights[k].animate.set_stroke(GREEN),
                      outs[k].animate.set_color(GREEN), chip.pulse(GREEN), run_time=0.35)
        self._raw = False
        tag = VGroup(L("GENERAL AI", 18, ICE, spacing=8), L("FAST · VERSATILE", 11, GREY_B, spacing=4))
        tag.arrange(DOWN, buff=0.1).next_to(chip, UP, 0.35)
        self.play(FadeIn(tag, shift=UP * 0.1), run_time=0.35)
        self.hold(0.9)  # reading time for the use cases
        done = ins
        # … then a question about OUR business: the user becomes a chat window
        icon = icon_user(ICE).move_to(USER_POS)
        in_rail = rail([[IN_X, OUT_Y, 0], chip.port(LEFT)], DIMC, 2)
        out_rail = rail([chip.port(RIGHT), ANS_IN], DIMC, 2)
        self.morph(VGroup(done, outs, tag, branches), VGroup(icon, in_rail, out_rail))
        user = self.make_chat()
        self.play(FadeTransform(icon, user), run_time=0.55, rate_func=rate_functions.ease_in_out_cubic)
        q_txt = self.doc_to_question("OUR CAR PARKS · PARIS?")
        win = self.chat_win
        u_bub = VGroup(self.q_box, q_txt)
        q = VGroup()
        # the question goes from the chat to the chip
        p = self.packet(ICE)
        self.send(p, [[IN_X, OUT_Y, 0], chip.port(LEFT)], ICE, run_time=0.4)
        self.play(chip.pulse(), FadeOut(p), run_time=0.35)
        web = neon(globe(0.42, CYAN).move_to([2.2, 3.05, 0]), CYAN, 1.6)
        web_lbl = L("INTERNET", 11, CYAN, spacing=4).next_to(web, RIGHT, 0.2)
        top = chip.port(UP)
        web_pts = [top, [top[0], 3.05, 0], web.get_left()]
        web_rail = rail(web_pts, CYAN, 1.6)
        mem = L("MEMORY", 11, CYAN, spacing=4).next_to(chip, DOWN, 0.3)
        self.play(Create(web_rail), FadeIn(web), FadeIn(web_lbl), FadeIn(mem), chip.pulse(CYAN),
                  *self.show_pins(("UP", 0)), run_time=0.5)
        p = self.packet(CYAN)
        self.send(p, web_pts + list(reversed(web_pts))[1:], CYAN, run_time=0.55)
        self.remove(p)
        # the answer comes back into the chat
        a_box = RoundedRectangle(corner_radius=0.1, width=CHAT_W - 0.4, height=0.72).set_stroke(ORANGE, 1.4)
        a_box.set_fill(BODY, 1).move_to(win.get_corner(DL) + np.array([0.2, 0.2, 0]), aligned_edge=DL).set_z_index(4)
        p = self.packet(ORANGE)
        self.send(p, [chip.port(LEFT), [IN_X, OUT_Y, 0]], ORANGE, run_time=0.3)
        self.play(FadeOut(p), run_time=0.2)
        widths = [2.5, 2.1, 1.5]
        lines = VGroup(*[Line(LEFT * w / 2, RIGHT * w / 2).set_stroke(ORANGE, 2.0, 0.85) for w in widths])
        lines.arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(a_box).set_z_index(5)
        self.play(Create(a_box), LaggedStart(*[Create(l) for l in lines], lag_ratio=0.25), run_time=0.55)
        rng = np.random.default_rng(5)

        def num(v):
            return Text(f"~{v}", font=TITLE, font_size=32, color=ORANGE).move_to(a_box).set_z_index(5)

        cur = num(int(rng.integers(20, 90)))
        self.play(FadeTransform(lines, cur), run_time=0.45)
        for v in (int(rng.integers(90, 400)), int(rng.integers(10, 60)), ):
            nxt = num(v)
            self._raw = True
            self.play(FadeTransform(cur, nxt), run_time=0.25)
            self._raw = False
            cur = nxt
        final = VGroup(Text("?", font=LABEL, font_size=32, color=ORANGE),
                       L("SOURCE: WEB", 10, ORANGE, spacing=2)).arrange(RIGHT, buff=0.3).move_to(a_box).set_z_index(5)
        self.play(FadeTransform(cur, final), run_time=0.45)
        guess = VGroup(u_bub, a_box, final)
        self.hold(0.5)
        self.user, self.in_rail, self.out_rail = user, in_rail, out_rail   # reused in act 3
        self.q_box = None
        self.intro_bits = VGroup(web, web_lbl, web_rail, mem, guess)

    # --- 02 · Our reality: Paris -------------------------------------------------------------------------------
    def a2_our_data(self):
        M = MAP_C
        c = M + UP * 0.75
        periph = neon(Ellipse(width=7.6, height=4.2).move_to(c), ManimColor("#1B5C69"), 2)
        seine = neon(VMobject().set_points_smoothly([c + [-4.3, -0.3, 0], c + [-2.2, 0.7, 0], c + [-0.2, -0.1, 0],
                                                     c + [1.9, 0.6, 0], c + [4.3, -0.2, 0]]),
                     ManimColor("#1E7BFF"), 2.2)
        rng = np.random.default_rng(7)
        parks = VGroup()
        while len(parks) < 42:
            x, y = rng.uniform(-3.5, 3.5), rng.uniform(-1.9, 1.9)
            if (x / 3.55) ** 2 + (y / 1.95) ** 2 < 0.92 and all(np.linalg.norm(p.get_center() - (c + [x, y, 0])) > 0.42
                                                                 for p in parks):
                sq = RoundedRectangle(corner_radius=0.03, width=0.26, height=0.26).set_stroke(ICE, 1.4).set_fill(BODY, 1)
                parks.add(VGroup(sq, L("P", 8, ICE, spacing=0).move_to(sq)).move_to(c + [x, y, 0]))

        self.level_lbl = L("PARIS", 18, GREY_B, spacing=10).move_to(M + [-3.6, 3.15, 0])
        self.count = self.mag_count(0)
        self.count_lbl = L("OF CAR PARKS", 14, CYAN, spacing=6).move_to(M + [2.0, 3.15, 0], aligned_edge=LEFT)
        # storage: server racks lighting up level after level
        self.racks = VGroup(*[rack().move_to(M + [4.75 + 0.52 * (i % 4), 0.85 - 1.27 * (i // 4), 0])
                              for i in range(12)])
        self.racks_on = 0
        self.ev_count, self.st_count = self.mag_events(0), self.mag_storage(0)
        self.ev_lbl = L("OF EVENTS / DAY", 10, GREEN, spacing=3).move_to(M + [4.55, 2.45, 0], aligned_edge=LEFT)
        self.st_lbl = L("STORED", 10, ICE, spacing=3).move_to(M + [4.55, 1.7, 0], aligned_edge=LEFT)
        self.rack_lbl = L("DATABASES", 10, GREY_B, spacing=3).next_to(self.racks, DOWN, 0.12)\
            .align_to(self.racks, LEFT)
        self.pv(periph, seine, parks, self.level_lbl, self.count_lbl, self.racks, self.ev_lbl, self.st_lbl,
                self.rack_lbl)

        # 1 → 2: the chip stays at the top (PUBLIC); a dashed boundary opens our PRIVATE world below
        line = DashedLine([-7.1, SPLIT_Y, 0], [7.1, SPLIT_Y, 0], dash_length=0.12).set_stroke(GREY_B, 1.4)
        pub = L("PUBLIC", 11, CYAN, spacing=6).move_to([6.95, SPLIT_Y + 0.2, 0], aligned_edge=RIGHT)
        priv = L("PRIVATE", 11, GREY_B, spacing=6).move_to([6.95, SPLIT_Y - 0.22, 0], aligned_edge=RIGHT)
        self.play(FadeOut(self.intro_bits), Create(line), FadeTransform(self.public, pub), FadeIn(priv, shift=DOWN * 0.1),
                  run_time=1.1)
        self.chapter("02 · OUR REALITY", "Our reality")
        self.frontier = VGroup(line, pub, priv)

        # our world unfolds: the boundary rises like a screen, the private area rolls out below
        # and pushes the chip (and the user) up, into the background
        # the user gets a context: they work at Indigo
        self.badge = self.user_badge(0)
        self.play(*self.show_pins(("DOWN", 0)), FadeIn(self.badge, shift=UP * 0.1), run_time=0.4)
        self.pushed = VGroup(self.chip, self.user, self.in_rail, self.out_rail, self.badge)
        self.pushed.save_state()
        panel = Rectangle(width=FW + 0.4, height=SPLIT_Y + 4.2).set_fill(ManimColor("#03090E"), 1).set_stroke(width=0)
        panel.move_to([0, (SPLIT_Y - 4.2) / 2, 0]).set_z_index(-5)
        scan = VGroup(*[Line([-7.3, y, 0], [7.3, y, 0]).set_stroke(ManimColor("#0B2730"), 1) for y in
                        np.arange(-4.0, TOP_Y, 0.35)]).set_z_index(-4)
        glow = Line([-7.3, SPLIT_Y, 0], [7.3, SPLIT_Y, 0]).set_stroke(CYAN, 8, 0.18).set_z_index(-3)
        self.add(panel, glow)
        h_top = TOP_Y + 4.2
        self.play(panel.animate(rate_func=rate_functions.ease_in_out_cubic).stretch_to_fit_height(h_top)
                  .move_to([0, (TOP_Y - 4.2) / 2, 0]),
                  glow.animate(rate_func=rate_functions.ease_in_out_cubic).move_to([0, TOP_Y, 0]),
                  line.animate(rate_func=rate_functions.ease_in_out_cubic).move_to([0, TOP_Y, 0]),
                  pub.animate(rate_func=rate_functions.ease_in_out_cubic).move_to([6.95, TOP_Y + 0.2, 0], aligned_edge=RIGHT),
                  priv.animate(rate_func=rate_functions.ease_in_out_cubic).move_to([6.95, TOP_Y - 0.22, 0], aligned_edge=RIGHT),
                  self.pushed.animate(rate_func=rate_functions.ease_in_out_cubic).scale(PUSH["scale"])
                  .move_to(PUSH["to"]),
                  LaggedStart(*[Create(l) for l in scan], lag_ratio=0.04), run_time=1.6)
        beam_top = self.chip.port(DOWN)
        beam = DashedLine(beam_top, [beam_top[0], TOP_Y + 0.02, 0], dash_length=0.06).set_stroke(GREY_B, 1.4)
        self.play(Create(beam), run_time=0.4)
        self.play(Flash([beam_top[0], TOP_Y, 0], color=RED, flash_radius=0.22, line_length=0.08, num_lines=8),
                  self.chip.pulse(RED), run_time=0.5)
        self.unfold = VGroup(panel, scan, glow, beam)
        self.play(Create(periph), Create(seine), FadeIn(self.level_lbl), run_time=1.0)
        self.play(FadeIn(self.ev_count), FadeIn(self.st_count), FadeIn(self.ev_lbl), FadeIn(self.st_lbl),
                  FadeIn(self.rack_lbl), *self.fill_racks(0), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(p, scale=0.4) for p in parks], lag_ratio=0.03), FadeIn(self.count),
                  FadeIn(self.count_lbl), run_time=1.0)
        self.play(LaggedStart(*[Flash(p, color=CYAN, flash_radius=0.26, line_length=0.09, num_lines=6)
                                for p in parks[::2]], lag_ratio=0.04), run_time=0.6)
        self.paris = VGroup(periph, seine, parks)
        self.parks = parks

    @staticmethod
    def pp(p):
        """Map position → position in the private area of the screen."""
        return PV_DEST + PV_K * (np.array(p) - PV_REF)

    @staticmethod
    def pv(*mobs):
        """Place objects built around MAP_C in the private area (below the boundary)."""
        for m in mobs:
            m.scale(PV_K, about_point=PV_REF).shift(PV_DEST - PV_REF)
        return mobs[0] if len(mobs) == 1 else mobs

    def mag_count(self, k):
        return self.pv(L(PARKS_MAG[k], 22, CYAN, spacing=3, font=TITLE).move_to(MAP_C + [1.85, 3.17, 0],
                                                                                aligned_edge=RIGHT))

    @staticmethod
    def fit(m, w=2.35):
        return m.scale_to_fit_width(w) if m.width > w else m

    def mag_events(self, k):
        return self.pv(self.fit(L(EVENTS_MAG[k], 16, GREEN, spacing=2, font=TITLE)).move_to(MAP_C + [4.55, 2.72, 0],
                                                                                            aligned_edge=LEFT))

    def mag_storage(self, k):
        return self.pv(self.fit(L(STORAGE_MAG[k], 16, ICE, spacing=2, font=TITLE)).move_to(MAP_C + [4.55, 1.97, 0],
                                                                                          aligned_edge=LEFT))

    def fill_racks(self, k):
        """Light the racks of level k and grow the orders of magnitude (events, storage)."""
        n = RACKS[k]
        new = self.racks[self.racks_on:n]
        anims = []
        if k > 0:
            ev, st = self.mag_events(k), self.mag_storage(k)
            anims += [FadeTransform(self.ev_count, ev), FadeTransform(self.st_count, st)]
            self.ev_count, self.st_count = ev, st
        if len(new):
            anims.append(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in new], lag_ratio=0.15))
            anims.append(LaggedStart(*[AnimationGroup(r[0].animate.set_stroke(color=CYAN), r[1].animate.set_stroke(ICE),
                                                      LaggedStart(*[l.animate.set_fill(GREEN, 1) for l in r[2]],
                                                                  lag_ratio=0.2))
                                       for r in new], lag_ratio=0.2))
        self.racks_on = n
        return anims

    def to_servers(self, sources, n=24, seed=0):
        """While zooming out, data packets leave the map and rush to the lit racks."""
        rng = np.random.default_rng(seed)
        racks = [r for r in self.racks[:self.racks_on]] or [self.racks[0]]
        pk = []
        for k in range(n):
            src = sources[int(rng.integers(0, len(sources)))]
            r = racks[int(rng.integers(0, len(racks)))]
            d = self.packet(CYAN).scale(0.55).move_to(src.get_center())
            pk.append((d, r[2][int(rng.integers(0, 6))].get_center()))
        self.add(*[d for d, _ in pk])
        return [LaggedStart(*[d.animate(rate_func=rate_functions.ease_in_out_sine).move_to(t).scale(0.4)
                              .set_opacity(0) for d, t in pk], lag_ratio=0.03),
                LaggedStart(*[Indicate(r[2], color=WHITE, scale_factor=1.0) for r in racks], lag_ratio=0.1)]

    def set_level(self, k):
        new_lbl = L(LEVELS[k], 18, GREY_B, spacing=10).scale(PV_K).move_to(self.level_lbl)
        count = self.mag_count(k)
        anims = [FadeTransform(self.level_lbl, new_lbl), FadeTransform(self.count, count), *self.fill_racks(k)]
        self.level_lbl, self.count = new_lbl, count
        return anims

    # --- 02 · … then France and the world -------------------------------------------------------------------
    def a2_zoom_out(self):
        M = MAP_C
        rng = np.random.default_rng(11)
        # France: Paris folds into a dot on the map of France
        paris_pt = self.pp(ll(2.35, 48.85, FR_K, FR_C))
        france = neon(VMobject().set_points_as_corners([ll(lo, la, FR_K, FR_C) for lo, la in FRANCE]),
                      ManimColor("#1B5C69"), 2)
        fr_dots = VGroup(*[square_dot(ll(lo, la, FR_K, FR_C) + rng.normal(0, 0.09, 3) * [1, 1, 0])
                           for lo, la, n in FR_CITIES for _ in range(n)])
        self.pv(france, fr_dots)
        # one gesture: data goes to the servers while Paris folds into France
        self.play(*self.to_servers(self.parks, 28, seed=1),
                  FadeOut(self.paris, target_position=paris_pt, scale=0.03), Create(france), *self.set_level(1),
                  LaggedStart(Wait(0.4), *[FadeIn(d, scale=0.3) for d in fr_dots], lag_ratio=0.03),
                  run_time=1.4, rate_func=rate_functions.ease_in_out_sine)

        # World: France settles onto the globe
        R = 2.3
        world = neon(globe(R, ManimColor("#1B5C69")).move_to(MC), ManimColor("#1B5C69"), 1.6)
        eu_pt = self.pp(MC + np.array([0.26 * R, 0.53 * R, 0]))
        w_dots = VGroup(*[square_dot(MC + np.array([u * R, v * R, 0]), CYAN, 0.07) for u, v in WORLD_DOTS])
        self.pv(world, w_dots)
        # same gesture: France settles onto the globe while its data joins the servers
        self.play(*self.to_servers(fr_dots, 32, seed=2),
                  FadeOut(VGroup(france, fr_dots), target_position=eu_pt, scale=0.1), Create(world),
                  *self.set_level(2),
                  LaggedStart(Wait(0.5), *[FadeIn(d, scale=0.3) for d in w_dots], lag_ratio=0.04),
                  run_time=1.5, rate_func=rate_functions.ease_in_out_sine)
        self.hold(0.3)

        # all this data converges into systems… then tables
        systems = VGroup()
        for k, name in enumerate(SYSTEMS):
            box = RoundedRectangle(corner_radius=0.06, width=1.95, height=0.5).move_to(M + [-5.4 + 2.16 * k, -2.35, 0])
            systems.add(VGroup(neon(box, GREY_B, 1.2, fill=BODY), L(name, 11, GREY_B, spacing=2).move_to(box)))
        sys_lbl = L("DOZENS OF SYSTEMS · HUNDREDS OF TABLES", 14, GREY_B, spacing=4).next_to(systems, DOWN, 0.12)
        self.pv(systems, sys_lbl)
        # the globe pours into the servers…
        rack_c = self.racks.get_center()
        self.play(world.animate(rate_func=rate_functions.ease_in_cubic).scale(0.15).move_to(rack_c).set_opacity(0),
                  LaggedStart(*[d.animate.move_to(self.racks[i % 12].get_center()).set_opacity(0)
                                for i, d in enumerate(w_dots)], lag_ratio=0.03),
                  LaggedStart(*[Indicate(r[2], color=WHITE, scale_factor=1.0) for r in self.racks], lag_ratio=0.05),
                  run_time=1.1)
        self.remove(world, w_dots)
        # … the servers turn into systems…
        self.play(*[FadeTransform(VGroup(self.racks[2 * i], self.racks[2 * i + 1]), systems[i]) for i in range(6)],
                  FadeIn(sys_lbl), FadeOut(VGroup(self.rack_lbl, self.ev_count, self.ev_lbl, self.st_count,
                                                  self.st_lbl)), run_time=1.1)

        self.tables = VGroup()
        for name, x in zip(TABLES, TABLE_XS):
            t = Text(name, font=MONO, font_size=10, color=GREY_B)
            box = RoundedRectangle(corner_radius=0.05, width=t.width + 0.18, height=0.38)
            self.tables.add(VGroup(box.set_stroke(DIMC, 1.5).set_fill(BODY, 1), t).move_to([x, DATA_Y, 0]))
        src_of = [0, 0, 1, 1, 2, 2, 3, 3, 4, 5]  # each system bursts into several tables
        # … and the systems into raw tables; the map folds away, the boundary drops above the tables
        y = DATA_Y + 0.4
        line, pub, priv = self.frontier
        self.play(*[FadeTransform(systems[i], VGroup(*[self.tables[j] for j in range(10) if src_of[j] == i]))
                    for i in range(6)],
                  FadeOut(sys_lbl), FadeOut(VGroup(self.level_lbl, self.count, self.count_lbl)),
                  line.animate.move_to([0, y, 0]), pub.animate.move_to([6.95, y + 0.2, 0], aligned_edge=RIGHT),
                  priv.animate.move_to([6.95, y - 0.85, 0], aligned_edge=RIGHT),
                  self.pushed.animate(rate_func=rate_functions.ease_in_out_cubic).restore(),
                  self.unfold[0].animate.stretch_to_fit_height(0.01).move_to([0, -4.15, 0]),
                  FadeOut(self.unfold[1:]), run_time=2.4)
        self.remove(self.unfold)
        self.hold(0.8)
        self.play(line.animate.set_stroke(opacity=0.45), pub.animate.set_opacity(0.6), priv.animate.set_opacity(0.6),
                  run_time=0.5)
        self.vault = VGroup(line, pub, priv)

    # --- 03 · The problem: the AI wired onto the raw data ---------------------------------------------------------
    def a3_direct_access(self):
        self.chapter("03 · THE PROBLEM", "The problem")
        self.build_wiring()
        # the question arrives… and the circuit is drawn as it goes down to the tables (direct access)
        self.question = self.doc_to_question(QUESTION)
        self.ask()
        direct = L("DIRECT ACCESS TO TABLES", 12, RED, spacing=4).move_to([1.4, -0.45, 0])
        self.play(LaggedStart(*[Create(c) for c in self.chaos], lag_ratio=0.03),
                  *self.show_pins(("DOWN", -1), ("DOWN", 1)),
                  LaggedStart(*[FadeIn(j, scale=0.5) for j in self.joints], lag_ratio=0.1),
                  *[flash_along(c, ICE, 4, run_time=1.2) for c in self.chaos],
                  self.vault[0].animate.set_stroke(RED, opacity=0.8), FadeIn(direct), run_time=1.2)
        self.play(self.vault[0].animate.set_stroke(GREY_B, opacity=0.45), FadeOut(direct), run_time=0.5)

        # on the right: with no map, the chip picks straight from the tables (same frame as the act 04 tool call)
        (frame, title), grid, _ = self.table_panel()
        out_lit = self.out_rail.copy().set_stroke(RED, 2 * 0.65, 0.9).set_z_index(4)
        self.play(Create(frame), FadeIn(title), Create(out_lit), self.chip.pulse(),
                  *[c.animate.set_stroke(opacity=BOTTOM_DIM) for c in self.chaos],
                  self.joints.animate.set_opacity(BOTTOM_DIM), run_time=0.6)
        self.play(LaggedStart(*[TransformFromCopy(t, g) for t, g in zip(self.tables, grid)], lag_ratio=0.05),
                  run_time=0.8)
        self.p3, self.p3_grid, self.p3_rail = VGroup(frame, title), grid, out_lit
        self.p3_call, self.reply = VGroup(), None

    def build_wiring(self):
        """Red rails leaving the pins and branching like the tree of definitions."""
        red = lambda pts: rail(pts, RED, 1.6).set_stroke(opacity=0.75)
        self.seg1, self.seg2, self.seg3, self.cut_pts = VGroup(), VGroup(), [], []
        self.j1_pos, self.j2_pos = [], []
        for i, (pin_k, yb) in enumerate([(1, -0.38), (-1, -0.52)]):
            p, j1 = self.pin(pin_k), J1_POS[i]
            self.seg1.add(red([p, [p[0], yb, 0], [j1[0], yb, 0], j1 + UP * 0.16]))
            self.j1_pos.append(j1)
            for j in range(2):
                leaf = 2 * i + j
                j2 = np.array([j1[0] + (j - 0.5) * 2 * J2_DX, J2_Y, 0])
                self.j2_pos.append(j2)
                self.seg2.add(red([j1 + DOWN * 0.16, [j1[0], j1[1] - 0.38, 0], [j2[0], j1[1] - 0.38, 0],
                                   j2 + UP * 0.25]))
                lines = VGroup()
                for n, ti in enumerate(LEAF_TABLES[leaf]):
                    t = self.tables[ti]
                    y = -2.35 - 0.12 * ((leaf * 3 + n) % 5)
                    x0 = j2[0] + (n - (len(LEAF_TABLES[leaf]) - 1) / 2) * 0.12
                    lines.add(red([[x0, J2_Y - 0.25, 0], [x0, y, 0], [t.get_x(), y, 0], t.get_top()]))
                    self.cut_pts.append(np.array([t.get_x(), (y + t.get_top()[1]) / 2, 0]))
                self.seg3.append(lines)
        self.chaos = VGroup(*self.seg1, *self.seg2, *self.seg3)
        self.joints = VGroup(*[Square(0.12).set_fill(RED, 1).set_stroke(width=0).move_to(p)
                               for p in self.j1_pos + self.j2_pos])

    def build_tree(self):
        """The wiring junctions become the tree nodes (same positions)."""
        nodes1, nodes2, leaves = VGroup(), VGroup(), VGroup()
        for i, name in enumerate(TREE_L1):
            lbl = L(name, 10, ICE, spacing=2)
            box = RoundedRectangle(corner_radius=0.05, width=lbl.width + 0.3, height=0.32).move_to(self.j1_pos[i])
            nodes1.add(VGroup(neon(box, DIMC, 1.1, fill=BODY), lbl.move_to(box)))
            for j, name2 in enumerate(TREE_L2):
                leaf = 2 * i + j
                lbl2 = VGroup(L(name2, 8, ICE, spacing=2), Text(TREE_LEAVES[leaf], font=TITLE, font_size=14,
                                                                color=GREY_B)).arrange(DOWN, buff=0.05)
                box2 = RoundedRectangle(corner_radius=0.05, width=1.2, height=0.5).move_to(self.j2_pos[leaf])
                nodes2.add(VGroup(neon(box2, DIMC, 1.1, fill=BODY), lbl2.move_to(box2)))
                leaves.add(lbl2[1])
        return nodes1, nodes2, leaves

    def node_style(self, n, color, f, animate=True):
        """Colour + intensity of a tree node (neon halo, stroke, fill, text), without flattening the halos."""
        glow, core = n[0]
        targets = [(g, dict(color=color, opacity=self.PIN_OPS[j] * f)) for j, g in enumerate(glow)]
        targets.append((core, dict(color=color, opacity=f)))
        out = []
        for m, kw in targets:
            out.append(m.animate.set_stroke(**kw) if animate else m.set_stroke(**kw))
        out.append(core.animate.set_fill(opacity=f) if animate else core.set_fill(opacity=f))
        ft = max(f, TEXT_DIM)
        out.append(n[1].animate.set_opacity(ft) if animate else n[1].set_opacity(ft))
        return out

    def light_path(self, leaf, color):
        i = leaf // 2
        n1, n2, lv = self.tree
        on = {id(n1[i]), id(n2[leaf])}
        dim = [m.animate.set_stroke(RED, 1.6 * 0.65, BOTTOM_DIM) for m in self.chaos] + \
              [a for n in (*n1, *n2) for a in self.node_style(n, DIMC, BOTTOM_DIM)] + \
              [l.animate.set_color(GREY_B).set_opacity(TEXT_DIM) for l in lv] + \
              [t[0].animate.set_stroke(DIMC) for t in self.tables]
        lit = [self.seg1[i].animate.set_stroke(color, 2.4, 1), self.seg2[leaf].animate.set_stroke(color, 2.4, 1),
               *[m.animate.set_stroke(color, 2.4, 1) for m in self.seg3[leaf]],
               *self.node_style(n1[i], color, 1), *self.node_style(n2[leaf], color, 1),
               lv[leaf].animate.set_color(color).set_opacity(1),
               *[self.tables[ti][0].animate.set_stroke(color, 2) for ti in LEAF_TABLES[leaf]]]
        return dim, lit

    def a3_random_guesses(self):
        self.tree = self.build_tree()
        n1, n2, lv = self.tree
        for n in (*n1, *n2):  # the tree is born dimmed, like the wiring
            self.node_style(n, DIMC, BOTTOM_DIM, animate=False)

        count_txt = L("4 DEFINITIONS → 4 ANSWERS", 11, ORANGE, spacing=3).move_to([0.9, -1.35, 0])
        count = VGroup(BackgroundRectangle(count_txt, color=BLACK, fill_opacity=1, buff=0.04), count_txt)
        amb = VGroup()   # the ambiguity shows in the chat, instead of the 2nd answer
        intro = [LaggedStart(*[ReplacementTransform(self.joints[k], n) for k, n in enumerate([*n1, *n2])],
                             lag_ratio=0.08), FadeIn(count),
                 self.question.animate.set_color(ORANGE)]

        grid = self.p3_grid
        rng = np.random.default_rng(4)
        for k, leaf in enumerate(TRIES):
            if k > 0:
                self.ask(run_time=0.4)
            picks = LEAF_TABLES[leaf]
            # the chip picks tables at random: the selection jumps from cell to cell, then stops
            hops = [int(i) for i in rng.choice([i for i in range(10) if i not in picks], 6, replace=False)]
            reset = [g[0].animate.set_stroke(DIMC, 1.1, 1) for g in grid] + ([FadeOut(self.p3_call)] if k else [])
            self.play(*reset, run_time=0.2)
            self.play(Succession(*[grid[i][0].animate(rate_func=there_and_back).set_stroke(ORANGE, 2, 1)
                                   for i in hops], lag_ratio=1), run_time=0.8)
            call = self.direct_query(picks)
            self.play(*[grid[i][0].animate.set_stroke(ORANGE, 2, 1) for i in picks], FadeIn(call, shift=DOWN * 0.1),
                      run_time=0.4)
            self.p3_call = call
            dim, lit = self.light_path(leaf, ORANGE)
            if k == 0:  # 1st attempt: the tree is revealed and the path lights up in the same gesture
                self.play(*intro, run_time=0.9)
                self.play(*lit, run_time=0.5)
            else:
                self.play(*dim, run_time=0.25)
                self.play(*lit, run_time=0.5)
            path = [self.seg1[leaf // 2], self.seg2[leaf], *self.seg3[leaf]]
            self.play(*[flash_along(m, WHITE, 4, run_time=0.6) for m in path], run_time=0.6)
            # the answer arrives in the chat, with the randomly picked definition
            reply = self.chat_reply(GUESSES[k], f"{TREE_L1[leaf // 2]} · {TREE_L2[leaf % 2]}", color=ORANGE)
            self.play(FadeTransform(self.reply, reply) if self.reply else FadeIn(reply, shift=UP * 0.1), run_time=0.4)
            self.reply = reply
            self.hold(0.15)

        # no definition is enforced: anything is possible, so nothing is reliable
        amb_sub = L("AMBIGUOUS", 12, RED, spacing=6)
        amb_sub.next_to(self.chapter_lbl, DOWN, 0.14).align_to(self.chapter_lbl, LEFT).set_z_index(30)
        self.play(*[m.animate.set_stroke(RED, 1.6 * 0.65, BOTTOM_DIM) for m in self.chaos],
                  *[a for n in (*n1, *n2) for a in self.node_style(n, RED, BOTTOM_DIM)],
                  *[l.animate.set_color(RED).set_opacity(TEXT_DIM) for l in lv],
                  *[t[0].animate.set_stroke(DIMC) for t in self.tables],
                  count_txt.animate.set_color(RED), self.reply[0].animate.set_stroke(color=RED),
                  self.reply[1].animate.set_color(RED), FadeOut(self.p3_rail),
                  *[grid[i][0].animate.set_stroke(RED, 2, 1) for i in LEAF_TABLES[TRIES[-1]]],
                  *[c[0].animate.set_stroke(RED) for c in self.p3_call[0]],
                  *[c[1].animate.set_color(RED) for c in self.p3_call[0]], run_time=0.5)
        # the ambiguity leaves the answer and settles under the title "03 · THE PROBLEM"
        self.play(FadeTransform(self.reply.copy(), amb_sub, path_arc=PI / 6), run_time=0.7)
        self.amb_sub = amb_sub
        for _ in range(2):
            self.play(self.reply.animate.shift(RIGHT * 0.06), run_time=0.04)
            self.play(self.reply.animate.shift(LEFT * 0.12), run_time=0.04)
            self.play(self.reply.animate.shift(RIGHT * 0.06), run_time=0.04)
        self.hold(0.6)
        self.doubts = VGroup(*n1, *n2, count, amb)

    def a3_ambiguity(self):
        band = RoundedRectangle(corner_radius=0.12, width=13.2, height=1.08).move_to([0, BAND_Y, 0])
        c, w, h = FRAME
        # the harness frame rises above the chip to include the TOOLS step
        bottom, top = c[1] - h / 2, self.chip.get_top()[1] + TOOLS_H + 0.24
        left, right = -3.02, 3.5   # widened left and right for a readable TOOLS step
        box = RoundedRectangle(corner_radius=0.18, width=right - left, height=top - bottom)
        box.move_to([(left + right) / 2, (top + bottom) / 2, 0])
        self.band_shape, self.box_shape = band, box
        self.band_ph = DashedVMobject(band.copy().set_stroke(GREY_B, 1.5), num_dashes=100)
        s1 = L("SEMANTIC LAYER", 15, CYAN, spacing=8).next_to(band, UP, 0.08).align_to(band, LEFT).shift(RIGHT * 0.15)
        # 1 · each tree node becomes a "?"
        nodes = list(self.doubts[:6])
        qs = [Text("?", font=LABEL, font_size=24, color=RED).move_to(n) for n in nodes]
        self.play(*[FadeOut(m, scale=0.9) for m in self.doubts[6:]],
                  *[FadeTransform(n, q) for n, q in zip(nodes, qs)], Create(self.band_ph),
                  self.chaos.animate.set_stroke(opacity=0.12), self.question.animate.set_color(ICE), run_time=0.8,
                  rate_func=rate_functions.ease_in_out_cubic)
        # 2 · the "?" climb the wires and gather at the centre of the band
        mid = band.get_center()
        self.play(LaggedStart(*[q.animate(path_arc=PI / 5).move_to(mid + RIGHT * (k - 2.5) * 0.28).set_color(GREY_B)
                                for k, q in enumerate(qs)], lag_ratio=0.06), run_time=0.8)
        # 3 · they merge into "SEMANTIC LAYER"…
        s1_mid = s1.copy().scale(1.25).move_to(mid)
        self.play(FadeTransform(VGroup(*qs), s1_mid), run_time=0.6)
        self.hold(0.4)
        # 4 · … which rises to become the band title, the question takes its place
        sub1 = L("WHAT DOES OUR DATA MEAN?", 14, ICE, spacing=4).move_to(mid)
        self.play(TransformFromCopy(s1_mid, sub1), ReplacementTransform(s1_mid, s1), run_time=0.8)
        self.hold(0.9)
        self.sens_sub, self.sens_lbl = sub1, s1

    # --- 04 · MCP: meaning ---------------------------------------------------------------------------------------
    def a4_semantic_layer(self):
        band = neon(self.band_shape, CYAN, 2, fill=ManimColor("#021B21"))
        label = VGroup(L("MCP", 20, CYAN, spacing=6), L("MODEL CONTEXT PROTOCOL", 8, CYAN, spacing=1))
        label.arrange(DOWN, buff=0.06).move_to([-5.75, BAND_Y, 0])
        # the question finds its answer: the band turns green… then becomes the MCP
        green = neon(self.band_shape, GREEN, 2, fill=ManimColor("#03200F"))
        self.sens_sub.set_z_index(3)
        label.set_z_index(3)
        self.play(FadeOut(self.band_ph), FadeIn(green), self.sens_sub.animate.set_color(GREEN),
                  FadeOut(self.amb_sub), run_time=0.5)
        self.play(flash_along(self.band_shape, GREEN, 5, run_time=0.6), run_time=0.6)
        # the question rises and becomes the chapter title; the band becomes the MCP
        self.chapter("04 · WHAT DOES OUR DATA MEAN?", "What does our data mean?", src=self.sens_sub,
                     extra=[FadeOut(green), FadeIn(band), FadeIn(label)])
        self.play(self.chaos.animate.set_stroke(opacity=0.85), run_time=0.3)
        self.play(LaggedStart(*[Flash(pt, color=WHITE, flash_radius=0.3, line_length=0.12, num_lines=8)
                                for pt in self.cut_pts], lag_ratio=0.12),
                  LaggedStart(*[c.animate.set_stroke(opacity=0) for c in self.chaos], lag_ratio=0.12), run_time=1.1)
        self.remove(self.chaos)
        self.band, self.band_label = band, label

        # 5 domains, each wired straight to its tables (no tools on screen)
        nodes = VGroup()
        for name, src in CONCEPTS:
            lbl = L(name, 10, CYAN, spacing=2)
            box = RoundedRectangle(corner_radius=0.06, width=max(lbl.width + 0.3, 1.2), height=0.38)
            nodes.add(VGroup(neon(box, CYAN, 1.4, fill=BODY), lbl.move_to(box)))
        nodes.arrange(RIGHT, buff=0.28)
        nodes.move_to([(label.get_right()[0] + 0.3 + self.band_shape.get_right()[0] - 0.25) / 2, BAND_Y, 0])
        for n in nodes:
            n[1].set_z_index(2)
        self.play(LaggedStart(*[ReplacementTransform(self.tables[src][1].copy(), n[1], path_arc=-PI / 4)
                                for (name, src), n in zip(CONCEPTS, nodes)], lag_ratio=0.15), run_time=1.4)
        domain_tables = CONCEPT_TABLES
        # right-angle circuit rails: down, horizontal run (one level per rail), down to the table
        y_hi = self.band_shape.get_bottom()[1] - 0.06
        y_lo = self.tables[0].get_top()[1] + 0.08
        n_roots = sum(len(t) for t in domain_tables)
        roots, k = VGroup(), 0
        for i, tbls in enumerate(domain_tables):
            for n, tbl in enumerate(tbls):
                x0 = nodes[i].get_x() + (n - (len(tbls) - 1) / 2) * 0.14
                y = y_hi - (y_hi - y_lo) * (k + 0.5) / n_roots
                t = self.tables[tbl]
                roots.add(rail([[x0, nodes[i].get_bottom()[1], 0], [x0, y, 0], [t.get_x(), y, 0], t.get_top()],
                               CYAN, 1.6))
                k += 1
        top = self.chip.port(DOWN)
        band_top = self.band_shape.get_top()[1]
        y_in = band_top - 0.12
        self.trunk_pts = [top, [top[0], band_top, 0]]
        # paths inside the MCP: from the entry point to each domain, at right angles
        self.bus_pts = [[[top[0], band_top, 0], [top[0], y_in, 0], [n.get_x(), y_in, 0], n.get_top()] for n in nodes]
        self.trunk = rail(self.trunk_pts, CYAN, 2)
        # bus drawn without overlaps: one horizontal spine + one drop per domain
        xs = [n.get_x() for n in nodes] + [top[0]]
        spine = rail([[min(xs), y_in, 0], [max(xs), y_in, 0]], CYAN, 1.6)
        entry = rail([[top[0], band_top, 0], [top[0], y_in, 0]], CYAN, 1.6)
        drops = [rail([[n.get_x(), y_in, 0], n.get_top()], CYAN, 1.6) for n in nodes]
        self.bus = VGroup(entry, spine, *drops)
        paths = VGroup(*roots, *self.bus)
        self.play(LaggedStart(*[Create(n[0]) for n in nodes], lag_ratio=0.08),
                  LaggedStart(*[Create(r) for r in paths], lag_ratio=0.05), Create(self.trunk), run_time=1.0)
        # once drawn, all rails are dimmed
        self.play(*[m.animate.set_stroke(opacity=0.25) for m in (*paths, self.trunk)], run_time=0.4)
        self.nodes, self.roots = nodes, VGroup(roots)

        # call: chip → MCP → the right domain → its table; the path is drawn and stays lit
        used_k = CONCEPT_TABLES[SEL][0]
        occ, used = self.nodes[SEL], self.tables[used_k]
        link = roots[sum(len(t) for t in domain_tables[:SEL])]
        lit = VGroup(*[m.copy().set_stroke(WHITE, 2.4 * 0.65, 1) for m in (self.trunk, rail(self.bus_pts[SEL]), link)])
        lit.set_z_index(4)
        others = [*[n for k, n in enumerate(self.nodes) if k != SEL], *[t for k, t in enumerate(self.tables) if k != used_k]]

        # on the right, the old answer makes way for the tool call panel, linked to the chip
        panel, steps = self.tool_panel()
        out_lit = self.out_rail.copy().set_stroke(CYAN, 2 * 0.65, 1).set_z_index(4)
        self.play(ReplacementTransform(self.p3[0], panel[0]), FadeTransform(self.p3[1], panel[1]),
                  FadeOut(self.p3_grid), FadeOut(self.p3_call), Create(out_lit),
                  self.chip.pulse(CYAN), run_time=0.6)
        # ① the MCP exposes its domains: they rise into the panel
        grid = steps[0]
        self.play(LaggedStart(*[TransformFromCopy(n, g) for n, g in zip(self.nodes, grid)], lag_ratio=0.1),
                  run_time=0.8)
        # ② the chip picks PARKING SESSIONS (in the panel and in the MCP at the same time)
        self.play(grid[SEL][0].animate.set_stroke(WHITE, 2, 1), self.dim([g for k, g in enumerate(grid) if k != SEL], 0.3),
                  occ[0].animate.set_stroke(color=WHITE), self.dim(others, 0.3), run_time=0.5)
        # ③ the call leaves with its parameters; the path is drawn down to the table
        call1 = steps[1][0]
        self.play(self.chip.pulse(CYAN), run_time=0.3)
        self.llm_sends(call1[0], call1[0], CYAN)
        self.play(FadeIn(VGroup(*call1[1:]), shift=LEFT * 0.05), FadeIn(steps[1][1]), run_time=0.3)
        self.play(Succession(Create(lit[0]), Create(lit[1]), Create(lit[2]), lag_ratio=1),
                  used[0].animate.set_stroke(CYAN, 2), run_time=0.9)
        self.play(Flash(occ, color=CYAN, flash_radius=0.8, num_lines=10), lit.animate.set_stroke(CYAN),
                  grid[SEL][0].animate.set_stroke(CYAN, 1.6, 1), run_time=0.4)
        # the answer arrives in the chat, below the question
        reply = self.chat_reply(*GOOD)
        self.play(FadeTransform(self.reply, reply), occ[0].animate.set_stroke(color=CYAN), run_time=0.5)
        self.lit, self.reply = VGroup(lit, out_lit), reply
        self.mini = VGroup(panel, *steps)
        self.hold(0.9)

        # same question, new attempt: the conversation continues in the chat (like a real chat)
        alt = 0
        first = self.reply
        q2 = self.chat_bubble(QUESTION)
        q2.move_to([self.chat_win.get_right()[0] - 0.2, first.get_bottom()[1] - 0.14, 0], aligned_edge=UR)
        wrong = self.chat_reply(tr("0.74 M"), f"{tr('ON-STREET SESSIONS')} · 09/26", color=ORANGE)
        wrong.move_to([self.chat_win.get_left()[0] + 0.2, q2.get_bottom()[1] - 0.14, 0], aligned_edge=UL)
        top = self.chat_win.get_top()[1]
        tall = RoundedRectangle(corner_radius=0.14, width=CHAT_W, height=top - wrong.get_bottom()[1] + 0.18)
        tall.move_to([CHAT_C[0], top, 0], aligned_edge=UP)
        win2 = neon(tall, ICE, 1.6, fill=BODY).set_z_index(3)
        # the window grows, the 1st exchange fades, the same question is typed again
        self.play(Transform(self.user[0], win2),
                  self.dim([self.badge], 0),
                  first.animate.set_opacity(0.45),
                  self.q_box.animate.set_opacity(0.45), self.question.animate.set_opacity(0.45), run_time=0.4)
        self.badge.next_to(win2, UP, 0.16).align_to(win2, LEFT).shift(RIGHT * 0.1)
        self.play(FadeIn(q2[0], shift=LEFT * 0.1), self.dim([self.badge], 1), run_time=0.25)
        self._raw = True
        self.play(AddTextLetterByLetter(q2[1], time_per_char=0.02), run_time=0.5)
        self._raw = False
        self.ask(run_time=0.4)
        call = steps[1][0]
        call2 = VGroup(grid[alt].copy(), *[m.copy() for m in call[1:]]).arrange(RIGHT, buff=0.06).move_to(call)
        call2[0][0].set_stroke(ORANGE, 1.6, 1)
        call2[0][1].set_color(ORANGE).set_opacity(1)
        call2[0][0].set_fill(BODY, 1)
        alt_link = roots[sum(len(t) for t in domain_tables[:alt])]
        lit2 = VGroup(*[m.copy().set_stroke(ORANGE, 2.4 * 0.65, 1) for m in (self.trunk, rail(self.bus_pts[alt]), alt_link)])
        lit2.set_z_index(5)
        alt_t = self.tables[CONCEPT_TABLES[alt][0]]
        # this time the chip takes ON-STREET SESSIONS: the 1st path stays visible (dimmed), the 2nd is drawn next to it
        self.play(grid[SEL][0].animate.set_stroke(CYAN, 1.1, 0.5), self.dim([grid[alt]], 1.0),
                  grid[alt][0].animate.set_stroke(ORANGE, 2, 1), FadeOut(call[0]), self.chip.pulse(ORANGE),
                  lit.animate.set_stroke(CYAN, opacity=0.4), run_time=0.5)
        self.llm_sends(call2[0], call2[0], ORANGE)
        self.remove(*call[1:])
        self.add(call2)
        self.play(Succession(Create(lit2[0]), Create(lit2[1]), Create(lit2[2]), lag_ratio=1),
                  self.dim([self.nodes[alt], alt_t], 1.0), alt_t[0].animate.set_stroke(ORANGE, 2),
                  self.nodes[alt][0].animate.set_stroke(color=ORANGE), run_time=0.8)
        self.play(FadeIn(wrong, shift=UP * 0.1), run_time=0.4)
        # same question, two answers: ≠
        x = self.chat_win.get_right()[0] + 0.14
        y1, y2 = first.get_y(), wrong.get_y()
        bracket = VMobject().set_points_as_corners([[x - 0.1, y1, 0], [x, y1, 0], [x, y2, 0], [x - 0.1, y2, 0]])
        bracket.set_stroke(RED, 1.6)
        neq = Text("≠", font=TITLE, font_size=26, color=RED).next_to(bracket, RIGHT, 0.08)
        bracket.set_z_index(5)
        neq.set_z_index(5)
        self.play(Create(bracket), FadeIn(neq, scale=1.4), first.animate.set_opacity(1), run_time=0.4)
        self.hold(0.6)
        # end of the act: the activated circuits are dimmed again
        # the lit copies disappear: only the dimmed base rail remains (no stacked layers)
        self.play(FadeOut(lit), FadeOut(lit2), FadeOut(out_lit), alt_t[0].animate.set_stroke(DIMC, 1.5),
                  used[0].animate.set_stroke(DIMC, 1.5), self.nodes[alt][0].animate.set_stroke(color=CYAN),
                  occ[0].animate.set_stroke(color=CYAN), run_time=0.5)
        # the MCP is explained: the tables (and the public / private boundary) condense into one DATA rectangle
        dbox = RoundedRectangle(corner_radius=0.12, width=self.band_shape.width, height=0.8).move_to([0, DATA_Y, 0])
        data = VGroup(neon(dbox, CYAN, 1.6, fill=BODY), L("DATA", 12, CYAN, spacing=6).move_to(dbox))
        self.play(ReplacementTransform(self.tables, data), FadeOut(self.roots), FadeOut(self.vault), run_time=0.8)
        self.tables, self.roots, self.vault, self.data_box = VGroup(data), VGroup(), VGroup(), dbox
        self.reply, self.lit_ok, self.lit = wrong, VGroup(lit[0], lit[1]), VGroup(VGroup(), VGroup())
        self.p4_grid, self.p4_call, self.p4_alt = grid, call2, alt
        self.chat_extra = VGroup(first, q2, bracket, neq)
        self.mini = VGroup(panel, grid, VGroup(call2, steps[1][1]))

    def chat_bubble(self, text):
        """Question bubble (right side of the chat), text ready to be typed."""
        txt = L(text, 10, ICE, spacing=2)
        box = RoundedRectangle(corner_radius=0.1, width=txt.width + 0.36, height=txt.height + 0.24)
        box.set_fill(ManimColor("#0B2730"), 1).set_stroke(width=0)
        return VGroup(box, txt.move_to(box)).set_z_index(4)

    def llm_sends(self, chip_m, target, color):
        """The AI sends its choice: the pill leaves the chip, follows the line to the panel and lands."""
        fly = chip_m.copy().scale(0.85)
        x_in = ANS_IN[0] + 0.12
        route = [self.chip.port(RIGHT), [x_in, OUT_Y, 0], [x_in, target.get_y(), 0], target.get_left() + LEFT * 0.05]
        self.send(fly, route, color, run_time=0.8)
        self.play(fly.animate.scale(1 / 0.85).move_to(target), run_time=0.25)
        self.remove(fly)
        self.add(target)

    def panel_frame(self, text, icon, color, h=2.9):
        """Shared frame of the right-hand panels (act 03: no map · act 04: tool call · act 05: tools)."""
        w = 2.7
        left = ANS_IN[0]
        box = RoundedRectangle(corner_radius=0.12, width=w, height=h).move_to([left + w / 2, OUT_Y - 0.4, 0])
        frame = neon(box, color, 1.6, fill=BODY)
        title = VGroup(icon, L(text, 9, color, spacing=4))
        title.arrange(RIGHT, buff=0.12).move_to(box.get_corner(UL) + np.array([0.18, -0.24, 0]), aligned_edge=LEFT)
        return box, frame, title.set_z_index(3)

    def table_panel(self):
        """Act 03: the 10 raw tables the chip picks from at random."""
        die = RoundedRectangle(corner_radius=0.05, width=0.24, height=0.24).set_stroke(ORANGE, 1.4)
        die = VGroup(die, *[Dot(die.get_center() + d * 0.06, radius=0.018, color=ORANGE) for d in (UL, ORIGIN, DR)])
        box, frame, title = self.panel_frame("NO MAP", die, ORANGE)
        grid = VGroup()
        for name in TABLES:
            b = RoundedRectangle(corner_radius=0.04, width=1.15, height=0.22).set_stroke(DIMC, 1.1, 1).set_fill(BODY, 1)
            t = T_(name, font=MONO, font_size=8, color=ICE)
            grid.add(VGroup(b, t.move_to(b).set_z_index(2)))
        grid.arrange_in_grid(5, 2, buff=(0.1, 0.06)).move_to(box.get_center() + UP * 0.2)
        self.p3_box = box
        return (frame, title), grid, None

    def direct_query(self, picks):
        """Act 03: the query goes to the picked tables, with no definition."""
        chips = VGroup()
        for i in picks:
            t = T_(TABLES[i], font=MONO, font_size=7, color=ORANGE)
            b = RoundedRectangle(corner_radius=0.04, width=t.width + 0.12, height=0.2).set_stroke(ORANGE, 1, 1)
            chips.add(VGroup(b.set_fill(BODY, 1), t.move_to(b).set_z_index(2)))
        chips.arrange(RIGHT, buff=0.06)
        lbl = L("DIRECT QUERY", 7, GREY_B, spacing=2)
        call = VGroup(chips, lbl).arrange(DOWN, buff=0.1)
        return call.move_to(self.p3_box.get_bottom() + UP * 0.38).set_z_index(3)

    def tool_panel(self):
        """Tool call panel, on the right (instead of the answer box): ① domains ② choice ③ call."""
        box, frame, title = self.panel_frame("TOOL CALL", icon_tool_card(CYAN).scale(0.55).set_z_index(0), CYAN)
        grid = self.domain_grid().move_to(box.get_center() + UP * 0.45)
        pills = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.06, width=0.5, height=0.22).set_fill(CYAN, 0.18)
                                .set_stroke(CYAN, 1, 0.8), L(t, 7, ICE, spacing=1)) for t in ("PARIS", "09/26")])
        for pl in pills:
            pl[1].move_to(pl[0]).set_z_index(2)
        call = VGroup(grid[SEL].copy(), *pills).arrange(RIGHT, buff=0.06).move_to(box.get_center() + DOWN * 0.72)
        call[0][0].set_stroke(CYAN, 1.6, 1)
        sent = L("SENT TO MCP", 7, GREY_B, spacing=2).next_to(call, DOWN, 0.12)
        return VGroup(frame, title), [grid, VGroup(call, sent)]

    def tools_strip(self):
        """Harness TOOLS step: a wide, low strip sitting on the chip, with the MCP domains."""
        w, h = self.box_shape.width - 0.3, TOOLS_H
        box = RoundedRectangle(corner_radius=0.12, width=w, height=h)
        box.move_to([self.box_shape.get_x(), self.chip.get_top()[1] + 0.12 + h / 2, 0])
        frame = neon(box, ORANGE, 1.4, fill=BODY).set_z_index(6)
        title = VGroup(icon_list(ORANGE).scale(1.2), L("TOOLS", 10, ORANGE, spacing=4)).arrange(RIGHT, buff=0.12)
        title.move_to(box.get_corner(UL) + np.array([0.2, -0.24, 0]), aligned_edge=LEFT).set_z_index(7)
        cw = (w - 0.3 - 4 * 0.08) / 5
        grid = VGroup()
        for name, _ in CONCEPTS:
            words = tr(name).split()
            if len(words) > 1:  # long name: on two lines, split as evenly as possible
                k = min(range(1, len(words)), key=lambda i: abs(len(" ".join(words[:i])) - len(" ".join(words[i:]))))
                lbl = VGroup(L(" ".join(words[:k]), 9, CYAN, spacing=2), L(" ".join(words[k:]), 9, CYAN, spacing=2))
                lbl.arrange(DOWN, buff=0.06)
            else:
                lbl = L(words[0], 9, CYAN, spacing=2)
            if lbl.width > cw - 0.12:
                lbl.scale_to_fit_width(cw - 0.12)
            b_ = RoundedRectangle(corner_radius=0.05, width=cw, height=0.46).set_stroke(CYAN, 1.1, 0.8).set_fill(BODY, 1)
            grid.add(VGroup(b_, lbl.move_to(b_)))
        grid.arrange(RIGHT, buff=0.08)
        grid.move_to([box.get_x(), box.get_top()[1] - 0.48 - 0.23, 0]).set_z_index(7)
        return VGroup(frame, title, grid, box)

    def domain_grid(self):
        """The MCP domains as pills (right-hand panels)."""
        grid = VGroup()
        for name, _ in CONCEPTS:
            lbl = L(name, 7, CYAN, spacing=1)
            b = RoundedRectangle(corner_radius=0.05, width=1.2, height=0.28).set_stroke(CYAN, 1.1, 0.8).set_fill(BODY, 1)
            if lbl.width > 1.1:
                lbl.scale_to_fit_width(1.1)
            grid.add(VGroup(b, lbl.move_to(b).set_z_index(2)))
        return grid.arrange_in_grid(3, 2, buff=(0.1, 0.08), flow_order="rd")

    def chat_reply(self, main, sub, color=CYAN):
        """AI answer in the chat window, left-aligned below the question."""
        txt = VGroup(Text(main, font=TITLE, font_size=20, color=color), L(sub, 7, color, spacing=1))
        txt.arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        box = RoundedRectangle(corner_radius=0.1, width=txt.width + 0.36, height=txt.height + 0.24)
        box.set_fill(BODY, 1).set_stroke(color, 1.2, 0.9)
        pos = self.chat_win.get_corner(UL) + np.array([0.2, -1.0, 0])
        return VGroup(box, txt.move_to(box)).move_to(pos, aligned_edge=UL).set_z_index(4)


    # --- 05 · Harness: the code becomes a frame around the chip ---------------------------------------------------
    def a5_build_harness(self):
        self.chapter("05 · HARNESS → TRUST", "Harness: trust")
        self.background = [self.band, self.band_label, self.nodes, self.bus, self.trunk, self.lit, self.roots,
                           self.tables, self.vault, self.sens_lbl]
        # inside the harness the chip gets a little smaller: one step among others
        self.play(self.dim(self.background, 0.3), FadeOut(self.lit[1]), FadeOut(self.chat_extra[2:]),
                  self.chip.animate.scale(CHIP_IN_HARNESS), run_time=0.5)

        self.chip.size *= CHIP_IN_HARNESS   # the pins (port) follow the new size
        # the harness frame is drawn around the chip; the tool call panel becomes its TOOLS step
        self.gates = VGroup()
        for name, icon, pos, side in GATES:
            if name == "TRACE":  # the TRACE step is the audit log itself
                jp = RoundedRectangle(corner_radius=0.1, width=2.75, height=1.15).move_to(JOURNAL_C)
                jh = T_("audit.log", font=MONO, font_size=12, color=ORANGE)
                jh.move_to(jp.get_corner(UL) + [0.18, -0.2, 0], aligned_edge=UL)
                self.gates.add(VGroup(neon(jp, ORANGE, 1.6, fill=BODY), jh, VGroup(), VGroup()))
                self.log_top = jp.get_corner(UL) + [0.18, -0.5, 0]
                self.logs = VGroup()
                continue
            sq = RoundedRectangle(corner_radius=0.06, width=0.6, height=0.6).move_to(pos)
            lbl = L(name, 8, ORANGE, spacing=2).next_to(sq, side, 0.1)
            num = VGroup()   # no more step numbers
            self.gates.add(VGroup(neon(sq, ORANGE, 1.6, fill=BODY), icon(ORANGE).scale(0.85).move_to(sq), lbl, num))
        frame = neon(self.box_shape, ORANGE, 2)
        box = self.box_shape
        # title in the top-right corner of the screen, above harness.py
        title_x = (box.get_right()[0] + 0.25 + FW / 2 - 0.2) / 2
        label = L("HARNESS", 20, ORANGE, spacing=10).move_to([title_x, 3.68, 0])
        strip = self.tools_strip()
        pan, grid4, calls = self.mini
        self.play(Create(frame), FadeIn(label), 
                  ReplacementTransform(pan[0], strip[0]), FadeTransform(pan[1], strip[1]),
                  *[ReplacementTransform(g, s_) for g, s_ in zip(grid4, strip[2])], FadeOut(calls), run_time=1.2)
        self.strip = strip
        self.code = self.code_file()
        bgs = self.code[3]
        self.code_lines.set_opacity(0)   # the code is not readable yet: it shows as a "matrix" while the tests run
        bgs.set_opacity(0)
        self.play(LaggedStart(*[FadeIn(g, scale=0.85) for g in self.gates], lag_ratio=0.15),
                  FadeIn(self.code, shift=LEFT * 0.15), run_time=0.7)
        # tested and controlled: tests run in harness.py, then the counter settles into its header
        n_tests = 48
        t = ValueTracker(0)
        fbox = self.code[0]
        tl = L("TESTS", 11, GREY_B, spacing=4)
        count = always_redraw(lambda: Text(f"{int(t.get_value())}/{n_tests}", font=MONO, font_size=20,
                                           color=GREEN if t.get_value() >= n_tests else ICE)
                              .next_to(tl, RIGHT, 0.16).set_z_index(9))
        tl.move_to([fbox.get_x() - 0.45, fbox.get_y() - 0.1, 0]).set_z_index(9)
        bg = BackgroundRectangle(VGroup(tl, Text("48/48", font=MONO, font_size=20).next_to(tl, RIGHT, 0.16)),
                                 color=BODY, fill_opacity=0.9, buff=0.08).set_z_index(8)
        rng = np.random.default_rng(5)

        def matrix_line(i, k):  # a "matrix" line as long as instruction i
            txt = "".join(rng.choice(list("01")) if ch != " " else " " for ch in RUN_LINES[i])
            m = Text(txt, font=MONO, font_size=10, color=GREEN).set_opacity(0.55 + 0.4 * ((k + i) % 2))
            return m.move_to(self.code_lines[i], aligned_edge=LEFT)

        matrix = always_redraw(lambda: VGroup(*[matrix_line(i, int(t.get_value())) for i in range(len(RUN_LINES))]))
        self.add(matrix, count)
        self.play(FadeIn(bg), FadeIn(tl), t.animate(rate_func=linear).set_value(n_tests), run_time=0.7)
        count.clear_updaters()
        matrix.clear_updaters()
        tests = VGroup(tl, count)
        # tests passed: the matrix resolves into function names
        targets = self.code_lines.copy().set_opacity(1)
        self._raw = True   # quick pass: the matrix resolves while the counter settles
        self.play(*[FadeTransform(m, c_) for m, c_ in zip(matrix, targets)],
                  tests.animate.scale(0.5).move_to(fbox.get_corner(UR) + np.array([-0.16, -0.18, 0]), aligned_edge=UR),
                  FadeOut(bg), run_time=0.45)
        self._raw = False
        self.remove(*targets)
        self.code_lines.set_opacity(1)
        bgs.set_fill(opacity=0.85)
        self.tests = tests

        # the harness locks: input, output and data access
        L_, R_, B_ = box.get_left()[0], box.get_right()[0], box.get_bottom()[1]
        clamps = VGroup(
            RoundedRectangle(corner_radius=0.03, width=0.12, height=0.46).move_to([L_, OUT_Y, 0]),
            RoundedRectangle(corner_radius=0.03, width=0.12, height=0.46).move_to([R_, OUT_Y, 0]),
            RoundedRectangle(corner_radius=0.03, width=0.46, height=0.12).move_to([CHIP_POS[0], B_, 0]),
        ).set_fill(ORANGE, 1).set_stroke(width=0)
        self.play(LaggedStart(*[GrowFromCenter(c) for c in clamps], lag_ratio=0.2),
                  Flash(frame, color=ORANGE, flash_radius=3.2, num_lines=16), run_time=0.8)
        self.hold(0.5)
        self.frame, self.frame_label, self.clamps, self.tag = frame, label, clamps, VGroup()

        self.journal = self.gates[3]
        self.hold(0.4)

    def add_log(self, text, color):
        if getattr(self, "condensed", False):  # the audit log becomes just an icon
            return Wait(0.01)
        entry = T_(text, font=MONO, font_size=11, color=color)
        entry.move_to(self.log_top + DOWN * 0.25 * len(self.logs), aligned_edge=UL)
        self.logs.add(entry)
        return FadeIn(entry, shift=UP * 0.1)

    def gate_state(self, g, color):
        return [g[0].animate.set_stroke(color=color), g[1].animate.set_color(color)]

    def reset_gates(self):
        return [a for g in self.gates for a in self.gate_state(g, ORANGE)]

    def check(self, k, ok=True):
        """A module runs: its own visual effect + colour."""
        g = self.gates[k]
        c = g[0].get_center()
        fx = []
        if k == 0:  # format: a beam sweeps the module
            beam = Line(UP * 0.36, DOWN * 0.36).set_stroke(GREEN, 3).move_to(c + LEFT * 0.3)
            self.add(beam)
            fx = [beam.animate.shift(RIGHT * 0.6).set_stroke(opacity=0)]
        elif k == 1:  # scope: a ripple
            fx = [Broadcast(Circle(0.28, color=GREEN, stroke_width=2), focal_point=c, n_mobs=2)]
        elif k == 2 and ok:  # rights: the padlock opens
            fx = [g[1].animate(rate_func=there_and_back).shift(UP * 0.07)]
        anims = self.code_step(GATE_LINE[k]) if hasattr(self, "code_lines") else []
        return [*self.gate_state(g, GREEN if ok else RED), *fx, *anims]


    def code_file(self):
        """harness.py right of the harness: scrolling binary, and the instructions running live."""
        left = self.box_shape.get_right()[0] + 0.25
        w, h = FW / 2 - 0.2 - left, 2.7
        box = RoundedRectangle(corner_radius=0.1, width=w, height=h).move_to([left + w / 2, OUT_Y - 0.15, 0])
        frame = neon(box, ORANGE, 1.4, fill=BODY)
        head = T_("harness.py", font=MONO, font_size=11, color=ORANGE)
        head.move_to(box.get_corner(UL) + np.array([0.16, -0.18, 0]), aligned_edge=UL)
        rng = np.random.default_rng(11)
        y_top, y_bot = box.get_top()[1] - 0.42, box.get_bottom()[1] + 0.12
        n = 12
        step = (y_top - y_bot) / n
        binary = VGroup(*[Text(" ".join(str(int(b)) for b in rng.integers(0, 2, 26)), font=MONO, font_size=7,
                               color=ORANGE).set_opacity(0.16) for _ in range(n)])
        for i, r in enumerate(binary):
            r.move_to([box.get_x(), y_top - i * step, 0])

        def scroll(m, dt):  # the binary scrolls up in a loop
            for r in m:
                r.shift(UP * dt * 0.35)
                if r.get_y() > y_top:
                    r.shift(DOWN * step * n)
        binary.add_updater(scroll)
        lines = VGroup(*[Text(t, font=MONO, font_size=10, color=ICE) for t in RUN_LINES])
        lines.arrange(DOWN, buff=0.17, aligned_edge=LEFT)
        lines.move_to(box.get_corner(UL) + np.array([0.38, -0.5, 0]), aligned_edge=UL)
        bgs = VGroup(*[BackgroundRectangle(l_, color=BODY, fill_opacity=0.85, buff=0.03) for l_ in lines])
        cursor = Text("▸", font=MONO, font_size=10, color=ORANGE).next_to(lines[0], LEFT, 0.1).set_opacity(0)
        self.code_lines, self.code_cursor, self.code_on = lines, cursor, None
        return VGroup(frame, binary, head, bgs, lines, cursor)

    def code_step(self, i):
        """Line i runs: it lights up, the previous one turns green."""
        anims = []
        if self.code_on is not None and self.code_on != i:
            anims.append(self.code_lines[self.code_on].animate.set_color(GREEN))
        anims += [self.code_lines[i].animate.set_color(ORANGE),
                  self.code_cursor.animate.set_opacity(1).next_to(self.code_lines[i], LEFT, 0.1)]
        self.code_on = i
        return anims

    def code_reset(self):
        self.code_on = None
        return [*[l_.animate.set_color(ICE) for l_ in self.code_lines], self.code_cursor.animate.set_opacity(0)]

    def ask_format(self):
        """The question enters the harness: FORMAT checks it before it reaches the chip."""
        p = self.packet(ICE)
        g0 = self.gates[0][0].get_center()
        self.send(p, [[IN_X, OUT_Y, 0], g0], ICE, run_time=0.35)
        self.play(*self.check(0), run_time=0.35)
        self.send(p, [g0, self.chip.port(LEFT)], GREEN, run_time=0.3)
        self.play(self.chip.pulse(), FadeOut(p), run_time=0.4)

    def run(self, call_text, log, to_chat=False, ask=True, scope=None):
        """Question → chip → checked tool call → MCP → chip → checked answer → user."""
        if ask:
            self.ask_format()
            self.play(*self.code_step(1), Flash(self.strip[2][SEL], color=ORANGE, flash_radius=0.5), run_time=0.35)
        p = self.packet(CYAN)
        top = self.chip.port(DOWN)
        g1, g2 = self.gates[1][0].get_center(), self.gates[2][0].get_center()
        self.send(p, [top, g1], CYAN, run_time=0.3)
        if scope is not None:  # SCOPE does not know the zone: it calls the user's rights
            self.scope_lookup(scope)
        self.play(*self.check(1), run_time=0.35)
        self.send(p, [g1, g2], CYAN, run_time=0.3)
        self.play(*self.check(2), run_time=0.3)
        node = self.nodes[SEL]
        path = [g2, [CHIP_POS[0], BUS_Y, 0]] + self.bus_pts[SEL][1:]
        # the call reaches the MCP: the semantic layer lights up (the rails stay subtle)
        paths = [self.bus, self.trunk, self.lit, self.roots]
        rest = [m for m in self.background if all(m is not p_ for p_ in paths)]
        self.play(self.dim(rest, 1.0), self.dim(paths, 0.45), *self.code_step(4), run_time=0.35)
        self.send(p, path, CYAN, run_time=0.6)
        self.play(Flash(node, color=CYAN, flash_radius=0.8), run_time=0.35)
        # the MCP fetches the data, then goes back up
        down = [node.get_bottom(), [node.get_x(), self.data_box.get_top()[1], 0]]
        self.send(p, down, CYAN, run_time=0.35)
        self.play(Flash(p, color=CYAN, flash_radius=0.5, num_lines=8), run_time=0.3)
        self.send(p, list(reversed(down)), CYAN, run_time=0.35)
        self.send(p, list(reversed(path)) + [top], CYAN, run_time=0.7)
        self.play(self.chip.pulse(CYAN), run_time=0.35)
        g3 = self.gates[3][0].get_center()
        self.send(p, [self.chip.port(RIGHT), g3], GREEN, run_time=0.4)
        self.play(*self.check(3), self.add_log(*log), run_time=0.35)
        if not to_chat:
            self.send(p, [g3, ANS_IN], GREEN, run_time=0.35)
        self.play(FadeOut(p, scale=0.3), run_time=0.15)

    def a5_scoped_question(self):
        # harness TOOLS step, above the chip: it extracts the question's context, then checks the tools
        alt = self.p4_alt
        # new conversation: the chat empties and shrinks back, the same question is asked to the harness
        old = VGroup(self.chat_extra[:2], self.reply, self.q_box, self.question)
        self.play(old.animate.shift(UP * 0.3).set_opacity(0),
                  Transform(self.user[0], neon(self.chat_win, ICE, 1.6, fill=BODY).set_z_index(3)),
                  self.badge.animate.next_to(self.chat_win, DOWN, 0.16).align_to(self.chat_win, LEFT).shift(RIGHT * 0.1),
                  self.nodes[alt][0].animate.set_stroke(color=CYAN), FadeOut(self.lit[0]),
                  run_time=0.5)
        self.remove(old)
        self.q_box = None
        self.play(*self.code_reset(), run_time=0.2)
        # the director's question, with no zone: the harness has to derive it from their rights
        self.question = self.doc_to_question(QUESTION_ME)
        self.ask_format()
        frame, title, grid, box = self.strip
        for g in grid:
            g[0].set_stroke(CYAN, 1.1, 0.8)
            g[1].set_color(CYAN).set_opacity(1)
        descs = VGroup()
        for k, g in enumerate(grid):
            if k == SEL:
                d = L("DEFAULT · CAR PARKS", 8, ICE, spacing=1)
                if d.width > g.width - 0.08:
                    d.scale_to_fit_width(g.width - 0.08)
            else:
                d = VGroup(*[Line(LEFT * w_ / 2, RIGHT * w_ / 2).set_stroke(GREY_B, 1.2, 0.6) for w_ in (0.7, 0.45)])
                d.arrange(DOWN, buff=0.05, aligned_edge=LEFT)
            descs.add(d.next_to(g, DOWN, 0.09).align_to(g, LEFT).shift(RIGHT * 0.05))
        descs.set_z_index(7)
        # the harness checks the MCP tools and their descriptions
        self.play(LaggedStart(*[FadeIn(d, shift=DOWN * 0.04) for d in descs], lag_ratio=0.08), run_time=0.6)
        self.play(*self.code_step(1), run_time=0.25)
        # with the descriptions, the AI picks the right tool straight away
        scan = SurroundingRectangle(VGroup(grid[SEL], descs[SEL]), color=ORANGE, buff=0.03, corner_radius=0.05,
                                    stroke_width=1.6).set_z_index(8)
        self.play(Create(scan), run_time=0.3)
        # "parking sessions" = off-street by default: the context matches, the right tool is picked
        self.play(descs[SEL].animate.set_color(ORANGE), grid[SEL][0].animate.set_stroke(ORANGE, 2, 1),
                  Flash(grid[SEL], color=ORANGE, flash_radius=0.6, num_lines=10),
                  run_time=0.5)
        self.hold(0.6)
        self.play(FadeOut(VGroup(descs, scan)), descs[SEL].animate.set_color(GREY_B), run_time=0.4)
        self.run(CALL_OK, ("09:14 sessions · west OK", GREEN), to_chat=True, ask=False, scope=self.badge)
        right = self.chat_reply(tr("0.31 M"), tr("OFF-STREET · WEST ZONE · 09/26"), color=GREEN)
        self.ok = icon_check(GREEN, 0.5).next_to(right, RIGHT, 0.15).set_z_index(6)
        self.play(FadeIn(right, shift=UP * 0.1), Create(self.ok), Flash(right, color=GREEN, flash_radius=1.0),
                  FadeIn(self.lit_ok.set_stroke(CYAN, opacity=1)), run_time=0.6)
        self.reply = right
        self.hold(1.0)

    # --- End of act 05: the view condenses ------------------------------------------------------------------------
    def a5_condense(self):
        """End of act 05: the demonstration is done, the view condenses."""
        self.hold(0.8)
        self.play(*self.reset_gates(), FadeOut(self.lit_ok), run_time=0.4)
        self.condense()

    def condense(self):
        """End of act 05: everything is explained, the detail condenses into icons (big picture)."""
        chip, old = self.chip, self.box_shape
        cx = chip.get_x()

        def module(icon, pos):
            sq = RoundedRectangle(corner_radius=0.06, width=0.6, height=0.6).move_to(pos)
            return VGroup(neon(sq, ORANGE, 1.6, fill=BODY), icon.scale(0.85).move_to(pos), VGroup(), VGroup())

        tools_m = module(icon_list(ORANGE).scale(1.3), [cx, chip.get_top()[1] + 0.5, 0])
        log_m = module(icon_log(ORANGE), [chip.get_right()[0] + 0.6, OUT_Y, 0])
        left, right = old.get_left()[0], log_m.get_right()[0] + 0.4
        top, bottom = chip.get_top()[1] + 0.65, old.get_bottom()[1]   # no more TOOLS step in the frame
        box = RoundedRectangle(corner_radius=0.18, width=right - left, height=top - bottom)
        box.move_to([(left + right) / 2, (top + bottom) / 2, 0])
        tag = VGroup(icon_doc(ORANGE).scale(0.45), T_("harness.py", font=MONO, font_size=10, color=ORANGE))
        tag.arrange(RIGHT, buff=0.08).next_to(box, UP, 0.1).align_to(box, LEFT)
        label = self.frame_label
        lbl_t = label.copy().scale(0.75).move_to([box.get_x(), box.get_top()[1] - 0.28, 0])   # inside the frame
        tests_t = self.tests.copy().next_to(tag, RIGHT, 0.2)
        self.code[1].clear_updaters()
        # semantic layer: the 5 domains → one icon, the 10 tables → one database
        mid = (left + right) / 2
        band = RoundedRectangle(corner_radius=0.12, width=right - left, height=0.9).move_to([mid, BAND_Y, 0])
        layers = VGroup(*[RoundedRectangle(corner_radius=0.04, width=0.5, height=0.12).shift(UP * 0.1 * i)
                          for i in range(3)]).set_stroke(CYAN, 1.6).set_fill(BODY, 1)
        mcp_lbl = self.band_label.copy().move_to(band)
        # the data: one plain big rectangle
        db_box = RoundedRectangle(corner_radius=0.12, width=right - left, height=0.8).move_to([mid, DATA_Y, 0])
        db = VGroup(neon(db_box, CYAN, 1.6, fill=BODY), L("DATA", 12, CYAN, spacing=6).move_to(db_box))
        trunk = rail([chip.port(DOWN), [chip.port(DOWN)[0], band.get_top()[1], 0]], CYAN, 2).set_stroke(opacity=0.5)
        link = rail([band.get_bottom(), db.get_top() + UP * 0.05], CYAN, 1.6).set_stroke(opacity=0.5)
        L_, R_ = box.get_left()[0], box.get_right()[0]
        self.play(Transform(self.frame, neon(box, ORANGE, 2)), self.clamps[1].animate.move_to([R_, OUT_Y, 0]),
                  FadeOut(VGroup(self.strip[0], self.strip[1], self.strip[2])),
                  FadeTransform(VGroup(self.gates[3], self.logs), log_m), FadeOut(self.scope_pill),
                  FadeOut(self.code, scale=0.4, target_position=tag), FadeIn(tag, scale=1.6), Transform(label, lbl_t), Transform(self.tests, tests_t),
                  Transform(self.band, neon(band, CYAN, 2, fill=ManimColor("#021B21"))),
                  FadeOut(self.nodes), Transform(self.band_label, mcp_lbl), FadeOut(self.sens_lbl),
                  FadeOut(self.bus), FadeOut(self.roots), Transform(self.trunk, trunk),
                  ReplacementTransform(self.tables[0], db), FadeIn(link), run_time=1.6)
        self.gates.submobjects[3] = log_m
        self.box_shape, self.band_shape = box, band
        self.bus, self.roots, self.nodes, self.tables = VGroup(), VGroup(link), VGroup(), VGroup(db)
        self.tools_icon, self.tag, self.condensed = VGroup(), tag, True
        self.hold(1.0)

    def user_badge(self, k):
        """User identity, below the chat: pictogram + the first k items of their context."""
        head = Circle(0.055).set_stroke(ICE, 1.4)
        body = Arc(radius=0.11, start_angle=0, angle=PI).set_stroke(ICE, 1.4)
        icon = VGroup(head, body.next_to(head, DOWN, 0.02).flip(RIGHT))
        badge = VGroup(icon, self.badge_text(k)).arrange(RIGHT, buff=0.14)
        bg = BackgroundRectangle(badge, color=BLACK, fill_opacity=1, buff=0.06)
        badge.add_to_back(bg)
        badge = VGroup(icon, badge[2], bg)   # [0] pictogram, [1] text, [2] background (drawn underneath)
        badge.next_to(self.user[0], DOWN, 0.16).align_to(self.user[0], LEFT).shift(RIGHT * 0.1)
        icon.set_z_index(5)
        badge[1].set_z_index(5)
        bg.set_z_index(3)
        return badge

    def badge_text(self, k):
        return L(" · ".join(tr(x) for x in USER_CTX[k]), 9, ICE, spacing=3)

    def badge_grow(self, k, color=ICE):
        """The user's context gains an item (the new one lights up briefly)."""
        new = self.badge_text(k).set_color(color).next_to(self.badge[0], RIGHT, 0.14).set_z_index(5)
        bg = BackgroundRectangle(VGroup(self.badge[0], new), color=BLACK, fill_opacity=1, buff=0.06).set_z_index(3)
        return [Transform(self.badge[1], new), Transform(self.badge[2], bg)]


    def scope_lookup(self, badge):
        """SCOPE calls for the user's scope; the zone comes back and attaches to the module."""
        g = self.gates[1][0]
        x = (self.box_shape.get_left()[0] + self.chat_win.get_right()[0]) / 2
        route = [g.get_left(), [x, g.get_y(), 0], [x, badge.get_y(), 0], badge.get_right() + RIGHT * 0.08]
        q = self.packet(ORANGE)
        self.send(q, route, ORANGE, run_time=0.6)
        self.play(FadeOut(q), Flash(badge[0], color=ORANGE, flash_radius=0.35, num_lines=8),
                  *self.badge_grow(2), run_time=0.5)
        txt = L("WEST ZONE", 8, ORANGE, spacing=2)
        box = RoundedRectangle(corner_radius=0.06, width=txt.width + 0.22, height=0.24)
        pill = VGroup(box.set_fill(BODY, 1).set_stroke(ORANGE, 1.2, 1), txt.move_to(box)).set_z_index(8)
        dest = g.get_right() + RIGHT * (0.2 + pill.width / 2)
        self.send(pill, list(reversed(route)) + [dest], ORANGE, run_time=0.8)
        self.scope_pill = pill

    # --- 06 · Together -------------------------------------------------------------------------------------------
    def a6_together(self):
        """Big picture: chat → harness → MCP → data; the answer becomes tables, charts, reports."""
        self.chapter("06 · TOGETHER", "Together")
        box, band = self.box_shape, self.band_shape
        # the harness is explained: no more detail inside, only the frame around the AI
        self.play(FadeOut(VGroup(self.gates, self.tools_icon, self.tag, self.tests)), run_time=0.6)
        trust = L("TRUST", 14, ORANGE, spacing=8).next_to(box, RIGHT, 0.3).align_to(box, DOWN)
        sem = L("SEMANTIC LAYER", 14, CYAN, spacing=8).next_to(band, RIGHT, 0.3)
        # the whole circuit lights up once, then the two key ideas flash next to their block
        self.play(flash_along(self.in_rail, WHITE, 5, run_time=0.9), flash_along(self.trunk, WHITE, 5, run_time=0.9),
                  *[flash_along(r, WHITE, 5, run_time=0.9) for r in self.roots], self.chip.pulse(), run_time=0.9)
        self.play(flash_along(box, ORANGE, 6, time_width=0.4, run_time=0.8),
                  flash_along(band, CYAN, 6, time_width=0.4, run_time=0.8), run_time=0.8)
        # on the right: the answer turns into deliverables
        bars = VGroup(*[Rectangle(width=0.1, height=h).set_fill(GREEN, 0.8).set_stroke(width=0)
                        for h in (0.18, 0.32, 0.24, 0.42)]).arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
        outs = VGroup()
        for icon, name in [(icon_sheet(GREEN), "TABLES"), (bars, "CHARTS"), (icon_doc(GREEN), "REPORTS")]:
            outs.add(VGroup(icon, L(name, 9, GREEN, spacing=3)).arrange(DOWN, buff=0.15))
        outs.arrange(RIGHT, buff=0.5).move_to([(box.get_right()[0] + FW / 2) / 2 + 0.2, OUT_Y + 0.3, 0])
        eff = L("UNDERSTAND THE DATA BETTER", 12, GREEN, spacing=4).next_to(outs, DOWN, 0.45)
        self.play(self.reply.animate.shift(UP * 0.04), self.ok.animate.shift(UP * 0.04), run_time=0.2)
        src = self.reply.copy()
        self.play(src.animate.move_to(outs).scale(0.8), run_time=0.7)
        self.play(FadeOut(src, scale=0.6), LaggedStart(*[FadeIn(o, scale=0.8) for o in outs], lag_ratio=0.2),
                  run_time=0.9)
        # sent back to the user, in all these forms: they arrive in the chat
        back = VGroup(*[o[0].copy() for o in outs])
        dest = back.copy().scale(0.45).arrange(RIGHT, buff=0.22)
        dest.next_to(self.reply, DOWN, 0.06).align_to(self.reply, LEFT).set_z_index(6)
        back.set_z_index(6)
        self.play(LaggedStart(*[b.animate(path_arc=PI / 5).move_to(d).scale(0.45) for b, d in zip(back, dest)],
                              lag_ratio=0.15), flash_along(self.in_rail, GREEN, 5, run_time=1.0), run_time=1.1)
        self.play(Flash(self.user[0], color=GREEN, flash_radius=1.9, num_lines=14), run_time=0.7)
        self.hold(1.0)
        # last shot: the rectangles disappear and become the words that sum up the film
        w1 = L("TRUST", 26, ORANGE, spacing=10)
        w2 = L("SEMANTIC LAYER", 26, CYAN, spacing=10)
        w3 = L("RETRIEVING DYNAMIC DATA", 20, WHITE, spacing=8)
        words = VGroup(w1, w2, w3).arrange(DOWN, buff=0.55).move_to([0, 0.2, 0])
        harness = VGroup(self.frame, self.frame_label, self.clamps)
        mcp = VGroup(self.band, self.band_label)
        data = self.tables
        keep = {id(m) for g in (harness, mcp, data) for m in g.get_family()} | {id(self.chapter_lbl)}
        rest = [m for m in self.mobjects if id(m) not in keep and m is not self.chapter_lbl]
        self.play(*[FadeOut(m) for m in rest], run_time=0.7)
        # the three blocks re-centre, then turn into words
        self.play(VGroup(harness, mcp, data).animate.scale(0.8).move_to([0, 0.2, 0]), run_time=0.9)
        # the harness becomes TRUST; the MCP becomes SEMANTIC LAYER, then UNDERSTANDING
        self.play(FadeTransform(harness, w1), FadeTransform(mcp, w2), FadeOut(data, scale=0.8), run_time=1.2)
        self.hold(1.0)
        und = L("UNDERSTANDING", 26, CYAN, spacing=10).move_to(w2)
        self.play(FadeTransform(w2, und), run_time=0.9)
        self.hold(0.6)
        # and finally, underneath: retrieving dynamic data
        self.play(FadeIn(w3, shift=UP * 0.12), run_time=0.9)
        self.hold(3.0)


