""""AI - Retrieving dynamic data" — standalone film, TRON style, no speaker.

The general AI does not know our data; the MCP brings meaning (a semantic layer between the AI and the data) and the
Harness — code, versioned and tested, that frames the chip — brings trust. Business example: parking.

How to read this file
- `acts` (just below) is the storyboard: 6 acts, 35 beats, each with a one-line note. Start there.
- Each beat is a method `b_<name>` further down, in story order: the animation of that moment, played on the shared
  Stage `self.st` (film_stage.py). A beat ends where the viewer gets time to read (`hold`, in seconds).
- Text, business data and positions: film_data.py. Film-specific building blocks (map, wiring, panels, the harness
  run): film_pieces.py. Generic pieces come from the kit (studio/kit, see gallery/README.md).

    studio still ai_retrieving_dynamic_data           # one frame per beat (fast-forward)
    studio act ai_retrieving_dynamic_data harness     # one act, 480p loop page
    studio regress ai_retrieving_dynamic_data         # pixel-identical to the baseline (EN + FR)
"""

import numpy as np
from manim import *

from studio.engine import Act, Beat, FilmScene
from studio.kit.actors import Badge, Chat, Chip, CodeFile, Module, data_block, harness_clamps, harness_frame, packet
from studio.kit.layout import ANS_IN, BAND_Y, CHAT_C, CHAT_H, CHAT_W, CHIP_POS, DATA_Y, IN_X, OUT_Y, USER_POS
from studio.kit.motions import dim, morph, send, words_from_blocks
from studio.kit.primitives import (BODY, CYAN, DIMC, GREEN, ICE, LABEL, MONO, ORANGE, RED, TITLE, flash_along, globe,
                                   icon_check, icon_doc, icon_log, icon_sheet, icon_user, neon, rail, square_dot)

from film_data import *  # noqa: F401,F403  (FR, tr, L, T_, business data, layout, map)
from film_pieces import Pieces
from film_stage import Stage


class Film(FilmScene, Pieces):
    title = "AI - Retrieving dynamic data"
    FR = FR

    @property
    def acts(self):
        return [
            Act("ai", "01 · THE AI", "General AI", auto_chapter=False, beats=[
                Beat("sources", play=Film.b_sources, hold=0, note="Six public sources; PUBLIC DATA dimmed until relevant."),
                Beat("chip_born", play=Film.b_chip_born, hold=0.3,
                     note="Circuit weaving: rails from the sources draw the chip; the words melt into it."),
                Beat("use_cases", play=Film.b_use_cases, hold=0.9,
                     note="Sources → tasks and results; each example runs through, results turn green. GENERAL AI."),
                Beat("question", play=Film.b_question, hold=0,
                     note="The user becomes a chat window and asks about OUR car parks."),
                Beat("web_guess", play=Film.b_web_guess, hold=0.5,
                     note="The AI looks on the web, numbers flicker: ? · SOURCE: WEB."),
            ]),
            Act("reality", "02 · OUR REALITY", "Our reality", auto_chapter=False, beats=[
                Beat("boundary", play=Film.b_boundary, hold=0, note="A dashed boundary: PUBLIC above, PRIVATE below."),
                Beat("unfold", play=Film.b_unfold, hold=0,
                     note="Our world unfolds and pushes the chip up; the user gets a badge (INDIGO · USER)."),
                Beat("paris", play=Film.b_paris, hold=0, note="Paris: tens of car parks, events, storage, databases."),
                Beat("france_world", play=Film.b_france_world, hold=0.3,
                     note="Paris folds into France, France onto the globe; data rushes to the servers."),
                Beat("tables", play=Film.b_tables, hold=0.8,
                     note="Servers → systems → raw tables; the map folds away, the chip comes back."),
                Beat("vault", play=Film.b_vault, hold=0, note="The boundary dims: the tables are our private data."),
            ]),
            Act("problem", "03 · THE PROBLEM", "The problem", auto_chapter=False, beats=[
                Beat("direct_access", play=Film.b_direct_access, hold=0,
                     note="The question goes straight to the tables: red wiring, DIRECT ACCESS TO TABLES."),
                Beat("no_map", play=Film.b_no_map, hold=0, note="Right panel NO MAP: the 10 raw tables."),
                Beat("first_guess", play=Film.b_first_guess, hold=0.15,
                     note="Random pick; the wiring becomes the tree of definitions; a first answer in the chat."),
                Beat("second_guess", play=Film.b_second_guess, hold=0.15, note="Asked again: another definition, "
                                                                                 "another answer."),
                Beat("ambiguous", play=Film.b_ambiguous, hold=0.6, note="Everything turns red: AMBIGUOUS."),
                Beat("semantic_layer", play=Film.b_semantic_layer, hold=0.4,
                     note="The tree nodes become ?, climb into the band and merge into SEMANTIC LAYER."),
                Beat("our_question", play=Film.b_our_question, hold=0.9,
                     note="…which rises to the band title: WHAT DOES OUR DATA MEAN?"),
            ]),
            Act("mcp", "04 · WHAT DOES OUR DATA MEAN?", "What does our data mean?", auto_chapter=False, beats=[
                Beat("meaning", play=Film.b_meaning, hold=0,
                     note="The band turns green and becomes the MCP; the question becomes the chapter title."),
                Beat("domains", play=Film.b_domains, hold=0,
                     note="5 domains wired at right angles to their tables; rails dimmed once drawn."),
                Beat("tool_call", play=Film.b_tool_call, hold=0.9,
                     note="TOOL CALL panel: domains → choice → call; one path lit; the right answer in the chat."),
                Beat("second_ask", play=Film.b_second_ask, hold=0.6,
                     note="Same question again: ON-STREET this time — two answers, ≠."),
                Beat("data", play=Film.b_data, hold=0, note="Explained: the tables condense into one DATA block."),
            ]),
            Act("harness", "05 · HARNESS → TRUST", "Harness: trust", auto_chapter=False, beats=[
                Beat("harness_frame", play=Film.b_harness_frame, hold=0,
                     note="The chip shrinks; the harness frame is drawn; the tool panel becomes its TOOLS step."),
                Beat("tested", play=Film.b_tested, hold=0,
                     note="harness.py: tests run as a matrix (48/48), then resolve into function names."),
                Beat("locked", play=Film.b_locked, hold=0.5, note="The harness locks: input, output, data access."),
                Beat("director_asks", play=Film.b_director_asks, hold=0.6,
                     note="A director asks without a zone; the harness reads the tool descriptions, picks off-street."),
                Beat("scoped_call", play=Film.b_scoped_call, hold=1.0,
                     note="SCOPE fetches the user's zone (WEST); checked call → MCP → data → checked answer: 0.31 M ✓."),
                Beat("condense", play=Film.b_condense, hold=1.0,
                     note="Explained: the detail condenses into icons (harness · MCP · DATA)."),
            ]),
            Act("together", "06 · TOGETHER", "Together", auto_chapter=False, beats=[
                Beat("big_picture", play=Film.b_big_picture, hold=0,
                     note="Only the frame remains; the whole circuit lights up once."),
                Beat("deliverables", play=Film.b_deliverables, hold=0,
                     note="The answer becomes tables, charts, reports."),
                Beat("back_to_user", play=Film.b_back_to_user, hold=1.0, note="…sent back to the user, in the chat."),
                Beat("trust_meaning", play=Film.b_trust_meaning, hold=1.0,
                     note="Only the blocks remain; harness → TRUST, MCP → SEMANTIC LAYER."),
                Beat("understanding", play=Film.b_understanding, hold=0.6, note="SEMANTIC LAYER → UNDERSTANDING."),
                Beat("retrieving", play=Film.b_retrieving, hold=3.0, note="End on words: RETRIEVING DYNAMIC DATA."),
            ]),
        ]

    def build_stage(self):
        self.st = Stage()
        return self.st

    # =============================================================================================================
    # 01 · The AI: trained on the world, then general-purpose… but not on our data
    # =============================================================================================================
    def b_sources(self):
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
        self.st.sources, self.st.public = sources, public

    def b_chip_born(self):
        sources, public = self.st.sources, self.st.public
        # circuit weaving: each source sends right-angle rails towards the chip;
        # on arrival the rails draw the outline, then the core, then the pins; the words slide
        # along their rail and melt into the chip
        self.st.chip = chip = Chip(label_text=tr("AI")).move_to(CHIP_POS)
        chip.hide_pins()
        traces, words = VGroup(), []
        for k, src in enumerate(sources):
            col, row = divmod(k, 3)
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
        self.play(Create(chip.die), Create(chip.pins, lag_ratio=0.05), *chip.show_pins(*pins_used), run_time=0.6)
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
        self.st.traces = traces

    def b_use_cases(self):
        # a general intelligence: tasks and their results grow out of the chip, along rails
        c, chip, public = CHIP_POS, self.st.chip, self.st.public
        tasks = [("WRITE A CLIENT EMAIL", "EMAIL READY"), ("SUMMARISE A CONTRACT", "5 KEY POINTS"),
                 ("WRITE AN EXCEL FORMULA", "FORMULA")]
        ins, outs, branches = VGroup(), VGroup(), VGroup()
        self.play(public.animate.set_opacity(0.3), run_time=0.3)  # "PUBLIC DATA" stays until act 2
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
        srcs, trs = self.st.sources, self.st.traces
        self.play(*[FadeTransform(srcs[k], ins[k]) for k in range(3)],
                  *[FadeTransform(srcs[3 + k], outs[k]) for k in range(3)],
                  *[ReplacementTransform(trs[k], lefts[k]) for k in range(3)],
                  *[ReplacementTransform(trs[3 + k], rights[k]) for k in range(3)],
                  run_time=0.9, rate_func=rate_functions.ease_in_out_cubic)
        with self.exact():
            for k in range(3):  # each example runs through the circuit: the rail and the result turn green (match)
                self.play(lefts[k].animate.set_stroke(GREEN), rights[k].animate.set_stroke(GREEN),
                          outs[k].animate.set_color(GREEN), chip.pulse(GREEN), run_time=0.35)
        tag = VGroup(L("GENERAL AI", 18, ICE, spacing=8), L("FAST · VERSATILE", 11, GREY_B, spacing=4))
        tag.arrange(DOWN, buff=0.1).next_to(chip, UP, 0.35)
        self.play(FadeIn(tag, shift=UP * 0.1), run_time=0.35)
        self.st.use_cases = VGroup(ins, outs, tag, branches)

    def b_question(self):
        # … then a question about OUR business: the user becomes a chat window
        chip = self.st.chip
        done, outs, tag, branches = self.st.use_cases
        icon = icon_user(ICE).move_to(USER_POS)
        in_rail = rail([[IN_X, OUT_Y, 0], chip.port(LEFT)], DIMC, 2)
        out_rail = rail([chip.port(RIGHT), ANS_IN], DIMC, 2)
        morph(self, VGroup(done, outs, tag, branches), VGroup(icon, in_rail, out_rail))
        self.st.user = user = Chat(CHAT_C, CHAT_W, CHAT_H, tr("CHAT · AI"))
        self.play(FadeTransform(icon, user), run_time=0.55, rate_func=rate_functions.ease_in_out_cubic)
        q_txt = user.type_question(self, tr("OUR CAR PARKS · PARIS?"))
        self.st.u_bub = VGroup(user.q_box, q_txt)
        # the question goes from the chat to the chip
        p = packet(ICE)
        send(self, p, [[IN_X, OUT_Y, 0], chip.port(LEFT)], ICE, run_time=0.4)
        self.play(chip.pulse(), FadeOut(p), run_time=0.35)
        self.st.in_rail, self.st.out_rail = in_rail, out_rail   # reused until the end

    def b_web_guess(self):
        chip, win = self.st.chip, self.st.user.win
        web = neon(globe(0.42, CYAN).move_to([2.2, 3.05, 0]), CYAN, 1.6)
        web_lbl = L("INTERNET", 11, CYAN, spacing=4).next_to(web, RIGHT, 0.2)
        top = chip.port(UP)
        web_pts = [top, [top[0], 3.05, 0], web.get_left()]
        web_rail = rail(web_pts, CYAN, 1.6)
        mem = L("MEMORY", 11, CYAN, spacing=4).next_to(chip, DOWN, 0.3)
        self.play(Create(web_rail), FadeIn(web), FadeIn(web_lbl), FadeIn(mem), chip.pulse(CYAN),
                  *chip.show_pins(("UP", 0)), run_time=0.5)
        p = packet(CYAN)
        send(self, p, web_pts + list(reversed(web_pts))[1:], CYAN, run_time=0.55)
        self.remove(p)
        # the answer comes back into the chat
        a_box = RoundedRectangle(corner_radius=0.1, width=CHAT_W - 0.4, height=0.72).set_stroke(ORANGE, 1.4)
        a_box.set_fill(BODY, 1).move_to(win.get_corner(DL) + np.array([0.2, 0.2, 0]), aligned_edge=DL).set_z_index(4)
        p = packet(ORANGE)
        send(self, p, [chip.port(LEFT), [IN_X, OUT_Y, 0]], ORANGE, run_time=0.3)
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
            with self.exact():
                self.play(FadeTransform(cur, nxt), run_time=0.25)
            cur = nxt
        final = VGroup(Text("?", font=LABEL, font_size=32, color=ORANGE),
                       L("SOURCE: WEB", 10, ORANGE, spacing=2)).arrange(RIGHT, buff=0.3).move_to(a_box).set_z_index(5)
        self.play(FadeTransform(cur, final), run_time=0.45)
        guess = VGroup(self.st.u_bub, a_box, final)
        self.st.user.q_box = None
        self.st.intro_bits = VGroup(web, web_lbl, web_rail, mem, guess)

    # =============================================================================================================
    # 02 · Our reality: Paris, France, the world — then systems and raw tables
    # =============================================================================================================
    def b_boundary(self):
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

        self.st.level_lbl = L("PARIS", 18, GREY_B, spacing=10).move_to(M + [-3.6, 3.15, 0])
        self.st.count = self.mag_count(0)
        self.st.count_lbl = L("OF CAR PARKS", 14, CYAN, spacing=6).move_to(M + [2.0, 3.15, 0], aligned_edge=LEFT)
        # storage: server racks lighting up level after level
        self.st.racks = VGroup(*[rack().move_to(M + [4.75 + 0.52 * (i % 4), 0.85 - 1.27 * (i // 4), 0])
                                 for i in range(12)])
        self.st.racks_on = 0
        self.st.ev_count, self.st.st_count = self.mag_events(0), self.mag_storage(0)
        self.st.ev_lbl = L("OF EVENTS / DAY", 10, GREEN, spacing=3).move_to(M + [4.55, 2.45, 0], aligned_edge=LEFT)
        self.st.st_lbl = L("STORED", 10, ICE, spacing=3).move_to(M + [4.55, 1.7, 0], aligned_edge=LEFT)
        self.st.rack_lbl = L("DATABASES", 10, GREY_B, spacing=3).next_to(self.st.racks, DOWN, 0.12)\
            .align_to(self.st.racks, LEFT)
        self.pv(periph, seine, parks, self.st.level_lbl, self.st.count_lbl, self.st.racks, self.st.ev_lbl,
                self.st.st_lbl, self.st.rack_lbl)
        self.st.paris, self.st.parks = VGroup(periph, seine, parks), parks

        # 1 → 2: the chip stays at the top (PUBLIC); a dashed boundary opens our PRIVATE world below
        line = DashedLine([-7.1, SPLIT_Y, 0], [7.1, SPLIT_Y, 0], dash_length=0.12).set_stroke(GREY_B, 1.4)
        pub = L("PUBLIC", 11, CYAN, spacing=6).move_to([6.95, SPLIT_Y + 0.2, 0], aligned_edge=RIGHT)
        priv = L("PRIVATE", 11, GREY_B, spacing=6).move_to([6.95, SPLIT_Y - 0.22, 0], aligned_edge=RIGHT)
        self.play(FadeOut(self.st.intro_bits), Create(line), FadeTransform(self.st.public, pub),
                  FadeIn(priv, shift=DOWN * 0.1), run_time=1.1)
        self.chapter("02 · OUR REALITY", "Our reality")
        self.st.frontier = VGroup(line, pub, priv)

    def b_unfold(self):
        # our world unfolds: the boundary rises like a screen, the private area rolls out below
        # and pushes the chip (and the user) up, into the background; the user gets a context: they work at Indigo
        line, pub, priv = self.st.frontier
        self.st.badge = Badge(self.badge_text(0), self.st.user[0])
        self.play(*self.st.chip.show_pins(("DOWN", 0)), FadeIn(self.st.badge, shift=UP * 0.1), run_time=0.4)
        self.st.pushed = VGroup(self.st.chip, self.st.user, self.st.in_rail, self.st.out_rail, self.st.badge)
        self.st.pushed.save_state()
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
                  self.st.pushed.animate(rate_func=rate_functions.ease_in_out_cubic).scale(PUSH["scale"])
                  .move_to(PUSH["to"]),
                  LaggedStart(*[Create(l) for l in scan], lag_ratio=0.04), run_time=1.6)
        beam_top = self.st.chip.port(DOWN)
        beam = DashedLine(beam_top, [beam_top[0], TOP_Y + 0.02, 0], dash_length=0.06).set_stroke(GREY_B, 1.4)
        self.play(Create(beam), run_time=0.4)
        self.play(Flash([beam_top[0], TOP_Y, 0], color=RED, flash_radius=0.22, line_length=0.08, num_lines=8),
                  self.st.chip.pulse(RED), run_time=0.5)
        self.st.unfold = VGroup(panel, scan, glow, beam)

    def b_paris(self):
        periph, seine, parks = self.st.paris
        self.play(Create(periph), Create(seine), FadeIn(self.st.level_lbl), run_time=1.0)
        self.play(FadeIn(self.st.ev_count), FadeIn(self.st.st_count), FadeIn(self.st.ev_lbl), FadeIn(self.st.st_lbl),
                  FadeIn(self.st.rack_lbl), *self.fill_racks(0), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(p, scale=0.4) for p in parks], lag_ratio=0.03), FadeIn(self.st.count),
                  FadeIn(self.st.count_lbl), run_time=1.0)
        self.play(LaggedStart(*[Flash(p, color=CYAN, flash_radius=0.26, line_length=0.09, num_lines=6)
                                for p in parks[::2]], lag_ratio=0.04), run_time=0.6)

    def b_france_world(self):
        rng = np.random.default_rng(11)
        # France: Paris folds into a dot on the map of France
        paris_pt = self.pp(ll(2.35, 48.85, FR_K, FR_C))
        france = neon(VMobject().set_points_as_corners([ll(lo, la, FR_K, FR_C) for lo, la in FRANCE]),
                      ManimColor("#1B5C69"), 2)
        fr_dots = VGroup(*[square_dot(ll(lo, la, FR_K, FR_C) + rng.normal(0, 0.09, 3) * [1, 1, 0])
                           for lo, la, n in FR_CITIES for _ in range(n)])
        self.pv(france, fr_dots)
        # one gesture: data goes to the servers while Paris folds into France
        self.play(*self.to_servers(self.st.parks, 28, seed=1),
                  FadeOut(self.st.paris, target_position=paris_pt, scale=0.03), Create(france), *self.set_level(1),
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
        self.st.world = VGroup(world, w_dots)

    def b_tables(self):
        # all this data converges into systems… then tables
        M = MAP_C
        world, w_dots = self.st.world
        systems = VGroup()
        for k, name in enumerate(SYSTEMS):
            box = RoundedRectangle(corner_radius=0.06, width=1.95, height=0.5).move_to(M + [-5.4 + 2.16 * k, -2.35, 0])
            systems.add(VGroup(neon(box, GREY_B, 1.2, fill=BODY), L(name, 11, GREY_B, spacing=2).move_to(box)))
        sys_lbl = L("DOZENS OF SYSTEMS · HUNDREDS OF TABLES", 14, GREY_B, spacing=4).next_to(systems, DOWN, 0.12)
        self.pv(systems, sys_lbl)
        # the globe pours into the servers…
        rack_c = self.st.racks.get_center()
        self.play(world.animate(rate_func=rate_functions.ease_in_cubic).scale(0.15).move_to(rack_c).set_opacity(0),
                  LaggedStart(*[d.animate.move_to(self.st.racks[i % 12].get_center()).set_opacity(0)
                                for i, d in enumerate(w_dots)], lag_ratio=0.03),
                  LaggedStart(*[Indicate(r[2], color=WHITE, scale_factor=1.0) for r in self.st.racks], lag_ratio=0.05),
                  run_time=1.1)
        self.remove(world, w_dots)
        # … the servers turn into systems…
        self.play(*[FadeTransform(VGroup(self.st.racks[2 * i], self.st.racks[2 * i + 1]), systems[i]) for i in range(6)],
                  FadeIn(sys_lbl), FadeOut(VGroup(self.st.rack_lbl, self.st.ev_count, self.st.ev_lbl, self.st.st_count,
                                                  self.st.st_lbl)), run_time=1.1)

        self.st.tables = VGroup()
        for name, x in zip(TABLES, TABLE_XS):
            t = Text(name, font=MONO, font_size=10, color=GREY_B)
            box = RoundedRectangle(corner_radius=0.05, width=t.width + 0.18, height=0.38)
            self.st.tables.add(VGroup(box.set_stroke(DIMC, 1.5).set_fill(BODY, 1), t).move_to([x, DATA_Y, 0]))
        src_of = [0, 0, 1, 1, 2, 2, 3, 3, 4, 5]  # each system bursts into several tables
        # … and the systems into raw tables; the map folds away, the boundary drops above the tables
        y = DATA_Y + 0.4
        line, pub, priv = self.st.frontier
        self.play(*[FadeTransform(systems[i], VGroup(*[self.st.tables[j] for j in range(10) if src_of[j] == i]))
                    for i in range(6)],
                  FadeOut(sys_lbl), FadeOut(VGroup(self.st.level_lbl, self.st.count, self.st.count_lbl)),
                  line.animate.move_to([0, y, 0]), pub.animate.move_to([6.95, y + 0.2, 0], aligned_edge=RIGHT),
                  priv.animate.move_to([6.95, y - 0.85, 0], aligned_edge=RIGHT),
                  self.st.pushed.animate(rate_func=rate_functions.ease_in_out_cubic).restore(),
                  self.st.unfold[0].animate.stretch_to_fit_height(0.01).move_to([0, -4.15, 0]),
                  FadeOut(self.st.unfold[1:]), run_time=2.4)
        self.remove(self.st.unfold)

    def b_vault(self):
        line, pub, priv = self.st.frontier
        self.play(line.animate.set_stroke(opacity=0.45), pub.animate.set_opacity(0.6), priv.animate.set_opacity(0.6),
                  run_time=0.5)
        self.st.vault = VGroup(line, pub, priv)

    # =============================================================================================================
    # 03 · The problem: the AI wired onto the raw data
    # =============================================================================================================
    def b_direct_access(self):
        self.chapter("03 · THE PROBLEM", "The problem")
        self.build_wiring()
        # the question arrives… and the circuit is drawn as it goes down to the tables (direct access)
        self.st.question = self.st.user.type_question(self, tr(QUESTION))
        self.ask()
        direct = L("DIRECT ACCESS TO TABLES", 12, RED, spacing=4).move_to([1.4, -0.45, 0])
        self.play(LaggedStart(*[Create(c) for c in self.st.chaos], lag_ratio=0.03),
                  *self.st.chip.show_pins(("DOWN", -1), ("DOWN", 1)),
                  LaggedStart(*[FadeIn(j, scale=0.5) for j in self.st.joints], lag_ratio=0.1),
                  *[flash_along(c, ICE, 4, run_time=1.2) for c in self.st.chaos],
                  self.st.vault[0].animate.set_stroke(RED, opacity=0.8), FadeIn(direct), run_time=1.2)
        self.play(self.st.vault[0].animate.set_stroke(GREY_B, opacity=0.45), FadeOut(direct), run_time=0.5)

    def b_no_map(self):
        # on the right: with no map, the chip picks straight from the tables (same frame as the act 04 tool call)
        (frame, title), grid, _ = self.table_panel()
        out_lit = self.st.out_rail.copy().set_stroke(RED, 2 * 0.65, 0.9).set_z_index(4)
        self.play(Create(frame), FadeIn(title), Create(out_lit), self.st.chip.pulse(),
                  *[c.animate.set_stroke(opacity=BOTTOM_DIM) for c in self.st.chaos],
                  self.st.joints.animate.set_opacity(BOTTOM_DIM), run_time=0.6)
        self.play(LaggedStart(*[TransformFromCopy(t, g) for t, g in zip(self.st.tables, grid)], lag_ratio=0.05),
                  run_time=0.8)
        self.st.p3, self.st.p3_grid, self.st.p3_rail = VGroup(frame, title), grid, out_lit
        self.st.p3_call, self.st.reply = VGroup(), None

    def b_first_guess(self):
        self.st.tree = self.build_tree()
        n1, n2, lv = self.st.tree
        for n in (*n1, *n2):  # the tree is born dimmed, like the wiring
            self.node_style(n, DIMC, BOTTOM_DIM, animate=False)
        count_txt = L("4 DEFINITIONS → 4 ANSWERS", 11, ORANGE, spacing=3).move_to([0.9, -1.35, 0])
        count = VGroup(BackgroundRectangle(count_txt, color=BLACK, fill_opacity=1, buff=0.04), count_txt)
        amb = VGroup()   # the ambiguity shows in the chat, instead of the 2nd answer
        intro = [LaggedStart(*[ReplacementTransform(self.st.joints[k], n) for k, n in enumerate([*n1, *n2])],
                             lag_ratio=0.08), FadeIn(count),
                 self.st.question.animate.set_color(ORANGE)]
        self.st.count_txt, self.st.doubts = count_txt, VGroup(*n1, *n2, count, amb)
        self.st.guess_rng = np.random.default_rng(4)
        self.guess(0, intro)

    def b_second_guess(self):
        self.guess(1)

    def guess(self, k, intro=None):
        """Attempt k: the chip picks tables at random, the tree path lights up, a (wrong) answer reaches the chat."""
        leaf, grid, rng = TRIES[k], self.st.p3_grid, self.st.guess_rng
        if k > 0:
            self.ask(run_time=0.4)
        picks = LEAF_TABLES[leaf]
        # the chip picks tables at random: the selection jumps from cell to cell, then stops
        hops = [int(i) for i in rng.choice([i for i in range(10) if i not in picks], 6, replace=False)]
        reset = [g[0].animate.set_stroke(DIMC, 1.1, 1) for g in grid] + ([FadeOut(self.st.p3_call)] if k else [])
        self.play(*reset, run_time=0.2)
        self.play(Succession(*[grid[i][0].animate(rate_func=there_and_back).set_stroke(ORANGE, 2, 1)
                               for i in hops], lag_ratio=1), run_time=0.8)
        call = self.direct_query(picks)
        self.play(*[grid[i][0].animate.set_stroke(ORANGE, 2, 1) for i in picks], FadeIn(call, shift=DOWN * 0.1),
                  run_time=0.4)
        self.st.p3_call = call
        dim_, lit = self.light_path(leaf, ORANGE)
        if k == 0:  # 1st attempt: the tree is revealed and the path lights up in the same gesture
            self.play(*intro, run_time=0.9)
            self.play(*lit, run_time=0.5)
        else:
            self.play(*dim_, run_time=0.25)
            self.play(*lit, run_time=0.5)
        path = [self.st.seg1[leaf // 2], self.st.seg2[leaf], *self.st.seg3[leaf]]
        self.play(*[flash_along(m, WHITE, 4, run_time=0.6) for m in path], run_time=0.6)
        # the answer arrives in the chat, with the randomly picked definition
        reply = self.chat_reply(GUESSES[k], f"{TREE_L1[leaf // 2]} · {TREE_L2[leaf % 2]}", color=ORANGE)
        self.play(FadeTransform(self.st.reply, reply) if self.st.reply else FadeIn(reply, shift=UP * 0.1), run_time=0.4)
        self.st.reply = reply

    def b_ambiguous(self):
        # no definition is enforced: anything is possible, so nothing is reliable
        n1, n2, lv = self.st.tree
        grid = self.st.p3_grid
        amb_sub = L("AMBIGUOUS", 12, RED, spacing=6)
        amb_sub.next_to(self.chapter_lbl, DOWN, 0.14).align_to(self.chapter_lbl, LEFT).set_z_index(30)
        self.play(*[m.animate.set_stroke(RED, 1.6 * 0.65, BOTTOM_DIM) for m in self.st.chaos],
                  *[a for n in (*n1, *n2) for a in self.node_style(n, RED, BOTTOM_DIM)],
                  *[l.animate.set_color(RED).set_opacity(TEXT_DIM) for l in lv],
                  *[t[0].animate.set_stroke(DIMC) for t in self.st.tables],
                  self.st.count_txt.animate.set_color(RED), self.st.reply[0].animate.set_stroke(color=RED),
                  self.st.reply[1].animate.set_color(RED), FadeOut(self.st.p3_rail),
                  *[grid[i][0].animate.set_stroke(RED, 2, 1) for i in LEAF_TABLES[TRIES[-1]]],
                  *[c[0].animate.set_stroke(RED) for c in self.st.p3_call[0]],
                  *[c[1].animate.set_color(RED) for c in self.st.p3_call[0]], run_time=0.5)
        # the ambiguity leaves the answer and settles under the title "03 · THE PROBLEM"
        self.play(FadeTransform(self.st.reply.copy(), amb_sub, path_arc=PI / 6), run_time=0.7)
        self.st.amb_sub = amb_sub
        for _ in range(2):
            self.play(self.st.reply.animate.shift(RIGHT * 0.06), run_time=0.04)
            self.play(self.st.reply.animate.shift(LEFT * 0.12), run_time=0.04)
            self.play(self.st.reply.animate.shift(RIGHT * 0.06), run_time=0.04)

    def b_semantic_layer(self):
        self.st.mcp = Band(13.2, 1.08, [0, BAND_Y, 0], tr("MCP"), tr("MODEL CONTEXT PROTOCOL"))
        band = self.st.mcp.shape
        c, w, h = FRAME
        # the harness frame rises above the chip to include the TOOLS step
        bottom, top = c[1] - h / 2, self.st.chip.get_top()[1] + TOOLS_H + 0.24
        left, right = -3.02, 3.5   # widened left and right for a readable TOOLS step
        box = RoundedRectangle(corner_radius=0.18, width=right - left, height=top - bottom)
        box.move_to([(left + right) / 2, (top + bottom) / 2, 0])
        self.st.band_shape, self.st.box_shape = band, box
        self.st.band_ph = DashedVMobject(band.copy().set_stroke(GREY_B, 1.5), num_dashes=100)
        s1 = L("SEMANTIC LAYER", 15, CYAN, spacing=8).next_to(band, UP, 0.08).align_to(band, LEFT).shift(RIGHT * 0.15)
        # 1 · each tree node becomes a "?"
        nodes = list(self.st.doubts[:6])
        qs = [Text("?", font=LABEL, font_size=24, color=RED).move_to(n) for n in nodes]
        self.play(*[FadeOut(m, scale=0.9) for m in self.st.doubts[6:]],
                  *[FadeTransform(n, q) for n, q in zip(nodes, qs)], Create(self.st.band_ph),
                  self.st.chaos.animate.set_stroke(opacity=0.12), self.st.question.animate.set_color(ICE), run_time=0.8,
                  rate_func=rate_functions.ease_in_out_cubic)
        # 2 · the "?" climb the wires and gather at the centre of the band
        mid = band.get_center()
        self.play(LaggedStart(*[q.animate(path_arc=PI / 5).move_to(mid + RIGHT * (k - 2.5) * 0.28).set_color(GREY_B)
                                for k, q in enumerate(qs)], lag_ratio=0.06), run_time=0.8)
        # 3 · they merge into "SEMANTIC LAYER"…
        s1_mid = s1.copy().scale(1.25).move_to(mid)
        self.play(FadeTransform(VGroup(*qs), s1_mid), run_time=0.6)
        self.st.sens_lbl, self.st.sens_mid = s1, s1_mid

    def b_our_question(self):
        # 4 · … which rises to become the band title, the question takes its place
        s1, s1_mid = self.st.sens_lbl, self.st.sens_mid
        sub1 = L("WHAT DOES OUR DATA MEAN?", 14, ICE, spacing=4).move_to(self.st.band_shape.get_center())
        self.play(TransformFromCopy(s1_mid, sub1), ReplacementTransform(s1_mid, s1), run_time=0.8)
        self.st.sens_sub = sub1

    # =============================================================================================================
    # 04 · What does our data mean? The MCP: meaning
    # =============================================================================================================
    def b_meaning(self):
        band = self.st.mcp.frame()
        label = self.st.mcp.label.move_to([-5.75, BAND_Y, 0])
        # the question finds its answer: the band turns green… then becomes the MCP
        green = self.st.mcp.frame(GREEN, ManimColor("#03200F"))
        self.st.sens_sub.set_z_index(3)
        label.set_z_index(3)
        self.play(FadeOut(self.st.band_ph), FadeIn(green), self.st.sens_sub.animate.set_color(GREEN),
                  FadeOut(self.st.amb_sub), run_time=0.5)
        self.play(flash_along(self.st.band_shape, GREEN, 5, run_time=0.6), run_time=0.6)
        # the question rises and becomes the chapter title; the band becomes the MCP
        self.chapter("04 · WHAT DOES OUR DATA MEAN?", "What does our data mean?", src=self.st.sens_sub,
                     extra=[FadeOut(green), FadeIn(band), FadeIn(label)])
        self.play(self.st.chaos.animate.set_stroke(opacity=0.85), run_time=0.3)
        self.play(LaggedStart(*[Flash(pt, color=WHITE, flash_radius=0.3, line_length=0.12, num_lines=8)
                                for pt in self.st.cut_pts], lag_ratio=0.12),
                  LaggedStart(*[c.animate.set_stroke(opacity=0) for c in self.st.chaos], lag_ratio=0.12), run_time=1.1)
        self.remove(self.st.chaos)
        self.st.band, self.st.band_label = band, label

    def b_domains(self):
        # 5 domains, each wired straight to its tables (no tools on screen)
        nodes = VGroup()
        for name, src in CONCEPTS:
            lbl = L(name, 10, CYAN, spacing=2)
            box = RoundedRectangle(corner_radius=0.06, width=max(lbl.width + 0.3, 1.2), height=0.38)
            nodes.add(VGroup(neon(box, CYAN, 1.4, fill=BODY), lbl.move_to(box)))
        nodes.arrange(RIGHT, buff=0.28)
        nodes.move_to([(self.st.band_label.get_right()[0] + 0.3 + self.st.band_shape.get_right()[0] - 0.25) / 2,
                       BAND_Y, 0])
        for n in nodes:
            n[1].set_z_index(2)
        self.play(LaggedStart(*[ReplacementTransform(self.st.tables[src][1].copy(), n[1], path_arc=-PI / 4)
                                for (name, src), n in zip(CONCEPTS, nodes)], lag_ratio=0.15), run_time=1.4)
        # right-angle circuit rails: down, horizontal run (one level per rail), down to the table
        y_hi = self.st.band_shape.get_bottom()[1] - 0.06
        y_lo = self.st.tables[0].get_top()[1] + 0.08
        n_roots = sum(len(t) for t in CONCEPT_TABLES)
        roots, k = VGroup(), 0
        for i, tbls in enumerate(CONCEPT_TABLES):
            for n, tbl in enumerate(tbls):
                x0 = nodes[i].get_x() + (n - (len(tbls) - 1) / 2) * 0.14
                y = y_hi - (y_hi - y_lo) * (k + 0.5) / n_roots
                t = self.st.tables[tbl]
                roots.add(rail([[x0, nodes[i].get_bottom()[1], 0], [x0, y, 0], [t.get_x(), y, 0], t.get_top()],
                               CYAN, 1.6))
                k += 1
        top = self.st.chip.port(DOWN)
        band_top = self.st.band_shape.get_top()[1]
        y_in = band_top - 0.12
        self.st.trunk_pts = [top, [top[0], band_top, 0]]
        # paths inside the MCP: from the entry point to each domain, at right angles
        self.st.bus_pts = [[[top[0], band_top, 0], [top[0], y_in, 0], [n.get_x(), y_in, 0], n.get_top()] for n in nodes]
        self.st.trunk = rail(self.st.trunk_pts, CYAN, 2)
        # bus drawn without overlaps: one horizontal spine + one drop per domain
        xs = [n.get_x() for n in nodes] + [top[0]]
        spine = rail([[min(xs), y_in, 0], [max(xs), y_in, 0]], CYAN, 1.6)
        entry = rail([[top[0], band_top, 0], [top[0], y_in, 0]], CYAN, 1.6)
        drops = [rail([[n.get_x(), y_in, 0], n.get_top()], CYAN, 1.6) for n in nodes]
        self.st.bus = VGroup(entry, spine, *drops)
        paths = VGroup(*roots, *self.st.bus)
        self.play(LaggedStart(*[Create(n[0]) for n in nodes], lag_ratio=0.08),
                  LaggedStart(*[Create(r) for r in paths], lag_ratio=0.05), Create(self.st.trunk), run_time=1.0)
        # once drawn, all rails are dimmed
        self.play(*[m.animate.set_stroke(opacity=0.25) for m in (*paths, self.st.trunk)], run_time=0.4)
        self.st.nodes, self.st.roots = nodes, VGroup(roots)

    def b_tool_call(self):
        # call: chip → MCP → the right domain → its table; the path is drawn and stays lit
        roots = self.st.roots[0]
        used_k = CONCEPT_TABLES[SEL][0]
        occ, used = self.st.nodes[SEL], self.st.tables[used_k]
        link = roots[sum(len(t) for t in CONCEPT_TABLES[:SEL])]
        lit = VGroup(*[m.copy().set_stroke(WHITE, 2.4 * 0.65, 1) for m in (self.st.trunk, rail(self.st.bus_pts[SEL]), link)])
        lit.set_z_index(4)
        others = [*[n for k, n in enumerate(self.st.nodes) if k != SEL],
                  *[t for k, t in enumerate(self.st.tables) if k != used_k]]

        # on the right, the old answer makes way for the tool call panel, linked to the chip
        panel, steps = self.tool_panel()
        out_lit = self.st.out_rail.copy().set_stroke(CYAN, 2 * 0.65, 1).set_z_index(4)
        self.play(ReplacementTransform(self.st.p3[0], panel[0]), FadeTransform(self.st.p3[1], panel[1]),
                  FadeOut(self.st.p3_grid), FadeOut(self.st.p3_call), Create(out_lit),
                  self.st.chip.pulse(CYAN), run_time=0.6)
        # ① the MCP exposes its domains: they rise into the panel
        grid = steps[0]
        self.play(LaggedStart(*[TransformFromCopy(n, g) for n, g in zip(self.st.nodes, grid)], lag_ratio=0.1),
                  run_time=0.8)
        # ② the chip picks PARKING SESSIONS (in the panel and in the MCP at the same time)
        self.play(grid[SEL][0].animate.set_stroke(WHITE, 2, 1), dim([g for k, g in enumerate(grid) if k != SEL], 0.3),
                  occ[0].animate.set_stroke(color=WHITE), dim(others, 0.3), run_time=0.5)
        # ③ the call leaves with its parameters; the path is drawn down to the table
        call1 = steps[1][0]
        self.play(self.st.chip.pulse(CYAN), run_time=0.3)
        self.llm_sends(call1[0], call1[0], CYAN)
        self.play(FadeIn(VGroup(*call1[1:]), shift=LEFT * 0.05), FadeIn(steps[1][1]), run_time=0.3)
        self.play(Succession(Create(lit[0]), Create(lit[1]), Create(lit[2]), lag_ratio=1),
                  used[0].animate.set_stroke(CYAN, 2), run_time=0.9)
        self.play(Flash(occ, color=CYAN, flash_radius=0.8, num_lines=10), lit.animate.set_stroke(CYAN),
                  grid[SEL][0].animate.set_stroke(CYAN, 1.6, 1), run_time=0.4)
        # the answer arrives in the chat, below the question
        reply = self.chat_reply(*GOOD)
        self.play(FadeTransform(self.st.reply, reply), occ[0].animate.set_stroke(color=CYAN), run_time=0.5)
        self.st.lit, self.st.reply = VGroup(lit, out_lit), reply
        self.st.mini = VGroup(panel, *steps)
        self.st.tool_steps, self.st.used_table = steps, used

    def b_second_ask(self):
        # same question, new attempt: the conversation continues in the chat (like a real chat)
        lit, out_lit = self.st.lit
        steps = self.st.tool_steps
        grid = steps[0]
        roots = self.st.roots[0]
        alt = 0
        first = self.st.reply
        q2 = Chat.bubble(tr(QUESTION))
        q2.move_to([self.st.user.win.get_right()[0] - 0.2, first.get_bottom()[1] - 0.14, 0], aligned_edge=UR)
        wrong = self.chat_reply(tr("0.74 M"), f"{tr('ON-STREET SESSIONS')} · 09/26", color=ORANGE)
        wrong.move_to([self.st.user.win.get_left()[0] + 0.2, q2.get_bottom()[1] - 0.14, 0], aligned_edge=UL)
        top = self.st.user.win.get_top()[1]
        tall = RoundedRectangle(corner_radius=0.14, width=CHAT_W, height=top - wrong.get_bottom()[1] + 0.18)
        tall.move_to([CHAT_C[0], top, 0], aligned_edge=UP)
        win2 = neon(tall, ICE, 1.6, fill=BODY).set_z_index(3)
        # the window grows, the 1st exchange fades, the same question is typed again
        self.play(Transform(self.st.user[0], win2),
                  dim([self.st.badge], 0),
                  first.animate.set_opacity(0.45),
                  self.st.user.q_box.animate.set_opacity(0.45), self.st.question.animate.set_opacity(0.45), run_time=0.4)
        self.st.badge.next_to(win2, UP, 0.16).align_to(win2, LEFT).shift(RIGHT * 0.1)
        self.play(FadeIn(q2[0], shift=LEFT * 0.1), dim([self.st.badge], 1), run_time=0.25)
        with self.exact():
            self.play(AddTextLetterByLetter(q2[1], time_per_char=0.02), run_time=0.5)
        self.ask(run_time=0.4)
        call = steps[1][0]
        call2 = VGroup(grid[alt].copy(), *[m.copy() for m in call[1:]]).arrange(RIGHT, buff=0.06).move_to(call)
        call2[0][0].set_stroke(ORANGE, 1.6, 1)
        call2[0][1].set_color(ORANGE).set_opacity(1)
        call2[0][0].set_fill(BODY, 1)
        alt_link = roots[sum(len(t) for t in CONCEPT_TABLES[:alt])]
        lit2 = VGroup(*[m.copy().set_stroke(ORANGE, 2.4 * 0.65, 1) for m in (self.st.trunk, rail(self.st.bus_pts[alt]), alt_link)])
        lit2.set_z_index(5)
        alt_t = self.st.tables[CONCEPT_TABLES[alt][0]]
        # this time the chip takes ON-STREET SESSIONS: the 1st path stays visible (dimmed), the 2nd is drawn next to it
        self.play(grid[SEL][0].animate.set_stroke(CYAN, 1.1, 0.5), dim([grid[alt]], 1.0),
                  grid[alt][0].animate.set_stroke(ORANGE, 2, 1), FadeOut(call[0]), self.st.chip.pulse(ORANGE),
                  lit.animate.set_stroke(CYAN, opacity=0.4), run_time=0.5)
        self.llm_sends(call2[0], call2[0], ORANGE)
        self.remove(*call[1:])
        self.add(call2)
        self.play(Succession(Create(lit2[0]), Create(lit2[1]), Create(lit2[2]), lag_ratio=1),
                  dim([self.st.nodes[alt], alt_t], 1.0), alt_t[0].animate.set_stroke(ORANGE, 2),
                  self.st.nodes[alt][0].animate.set_stroke(color=ORANGE), run_time=0.8)
        self.play(FadeIn(wrong, shift=UP * 0.1), run_time=0.4)
        # same question, two answers: ≠
        x = self.st.user.win.get_right()[0] + 0.14
        y1, y2 = first.get_y(), wrong.get_y()
        bracket = VMobject().set_points_as_corners([[x - 0.1, y1, 0], [x, y1, 0], [x, y2, 0], [x - 0.1, y2, 0]])
        bracket.set_stroke(RED, 1.6)
        neq = Text("≠", font=TITLE, font_size=26, color=RED).next_to(bracket, RIGHT, 0.08)
        bracket.set_z_index(5)
        neq.set_z_index(5)
        self.play(Create(bracket), FadeIn(neq, scale=1.4), first.animate.set_opacity(1), run_time=0.4)
        self.st.second = VGroup(lit2, alt_t, call2, wrong)
        self.st.chat_extra = VGroup(first, q2, bracket, neq)

    def b_data(self):
        # end of the act: the activated circuits are dimmed again
        # the lit copies disappear: only the dimmed base rail remains (no stacked layers)
        lit, out_lit = self.st.lit
        lit2, alt_t, call2, wrong = self.st.second
        alt, occ, steps = 0, self.st.nodes[SEL], self.st.tool_steps
        panel, grid = self.st.mini[0], steps[0]
        self.play(FadeOut(lit), FadeOut(lit2), FadeOut(out_lit), alt_t[0].animate.set_stroke(DIMC, 1.5),
                  self.st.used_table[0].animate.set_stroke(DIMC, 1.5), self.st.nodes[alt][0].animate.set_stroke(color=CYAN),
                  occ[0].animate.set_stroke(color=CYAN), run_time=0.5)
        # the MCP is explained: the tables (and the public / private boundary) condense into one DATA rectangle
        dbox, data = data_block(self.st.band_shape.width, [0, DATA_Y, 0], tr("DATA"))
        self.play(ReplacementTransform(self.st.tables, data), FadeOut(self.st.roots), FadeOut(self.st.vault), run_time=0.8)
        self.st.tables, self.st.roots, self.st.vault, self.st.data_box = VGroup(data), VGroup(), VGroup(), dbox
        self.st.reply, self.st.lit_ok, self.st.lit = wrong, VGroup(lit[0], lit[1]), VGroup(VGroup(), VGroup())
        self.st.p4_alt = alt
        self.st.mini = VGroup(panel, grid, VGroup(call2, steps[1][1]))

    # =============================================================================================================
    # 05 · Harness: the code becomes a frame around the chip
    # =============================================================================================================
    def b_harness_frame(self):
        self.chapter("05 · HARNESS → TRUST", "Harness: trust")
        self.st.background = [self.st.band, self.st.band_label, self.st.nodes, self.st.bus, self.st.trunk, self.st.lit,
                              self.st.roots, self.st.tables, self.st.vault, self.st.sens_lbl]
        # inside the harness the chip gets a little smaller: one step among others
        self.play(dim(self.st.background, 0.3), FadeOut(self.st.lit[1]), FadeOut(self.st.chat_extra[2:]),
                  self.st.chip.animate.scale(CHIP_IN_HARNESS), run_time=0.5)
        self.st.chip.size *= CHIP_IN_HARNESS   # the pins (port) follow the new size
        # the harness frame is drawn around the chip; the tool call panel becomes its TOOLS step
        self.st.gates = VGroup()
        for name, icon, pos, side in GATES:
            if name == "TRACE":  # the TRACE step is the audit log itself
                jp = RoundedRectangle(corner_radius=0.1, width=2.75, height=1.15).move_to(JOURNAL_C)
                jh = T_("audit.log", font=MONO, font_size=12, color=ORANGE)
                jh.move_to(jp.get_corner(UL) + [0.18, -0.2, 0], aligned_edge=UL)
                self.st.gates.add(VGroup(neon(jp, ORANGE, 1.6, fill=BODY), jh, VGroup(), VGroup()))
                self.st.log_top = jp.get_corner(UL) + [0.18, -0.5, 0]
                self.st.logs = VGroup()
                continue
            self.st.gates.add(Module(icon(ORANGE), pos, tr(name), side))
        frame = harness_frame(self.st.box_shape)
        box = self.st.box_shape
        # title in the top-right corner of the screen, above harness.py
        title_x = (box.get_right()[0] + 0.25 + FW / 2 - 0.2) / 2
        label = L("HARNESS", 20, ORANGE, spacing=10).move_to([title_x, 3.68, 0])
        strip = self.tools_strip()
        pan, grid4, calls = self.st.mini
        self.play(Create(frame), FadeIn(label),
                  ReplacementTransform(pan[0], strip[0]), FadeTransform(pan[1], strip[1]),
                  *[ReplacementTransform(g, s_) for g, s_ in zip(grid4, strip[2])], FadeOut(calls), run_time=1.2)
        self.st.strip, self.st.frame, self.st.frame_label = strip, frame, label

    def b_tested(self):
        self.st.code = CodeFile(self.st.box_shape.get_right()[0] + 0.25, FW / 2 - 0.2, OUT_Y - 0.15, RUN_LINES,
                                tr("harness.py"))
        bgs = self.st.code[3]
        self.st.code.lines.set_opacity(0)   # the code is not readable yet: it shows as a "matrix" while the tests run
        bgs.set_opacity(0)
        self.play(LaggedStart(*[FadeIn(g, scale=0.85) for g in self.st.gates], lag_ratio=0.15),
                  FadeIn(self.st.code, shift=LEFT * 0.15), run_time=0.7)
        # tested and controlled: tests run in harness.py, then the counter settles into its header
        n_tests = 48
        t = ValueTracker(0)
        fbox = self.st.code[0]
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
            return m.move_to(self.st.code.lines[i], aligned_edge=LEFT)

        matrix = always_redraw(lambda: VGroup(*[matrix_line(i, int(t.get_value())) for i in range(len(RUN_LINES))]))
        self.add(matrix, count)
        self.play(FadeIn(bg), FadeIn(tl), t.animate(rate_func=linear).set_value(n_tests), run_time=0.7)
        count.clear_updaters()
        matrix.clear_updaters()
        tests = VGroup(tl, count)
        # tests passed: the matrix resolves into function names
        targets = self.st.code.lines.copy().set_opacity(1)
        with self.exact():  # quick pass: the matrix resolves while the counter settles
            self.play(*[FadeTransform(m, c_) for m, c_ in zip(matrix, targets)],
                      tests.animate.scale(0.5).move_to(fbox.get_corner(UR) + np.array([-0.16, -0.18, 0]), aligned_edge=UR),
                      FadeOut(bg), run_time=0.45)
        self.remove(*targets)
        self.st.code.lines.set_opacity(1)
        bgs.set_fill(opacity=0.85)
        self.st.tests = tests

    def b_locked(self):
        # the harness locks: input, output and data access
        clamps = harness_clamps(self.st.box_shape, OUT_Y, CHIP_POS[0])
        self.play(LaggedStart(*[GrowFromCenter(c) for c in clamps], lag_ratio=0.2),
                  Flash(self.st.frame, color=ORANGE, flash_radius=3.2, num_lines=16), run_time=0.8)
        self.st.clamps, self.st.tag = clamps, VGroup()

    def b_director_asks(self):
        self.hold(0.4)   # the harness is built: a breath before the new question
        # harness TOOLS step, above the chip: it extracts the question's context, then checks the tools
        alt = self.st.p4_alt
        # new conversation: the chat empties and shrinks back, the same question is asked to the harness
        old = VGroup(self.st.chat_extra[:2], self.st.reply, self.st.user.q_box, self.st.question)
        self.play(old.animate.shift(UP * 0.3).set_opacity(0),
                  Transform(self.st.user[0], neon(self.st.user.win, ICE, 1.6, fill=BODY).set_z_index(3)),
                  self.st.badge.animate.next_to(self.st.user.win, DOWN, 0.16).align_to(self.st.user.win, LEFT)
                  .shift(RIGHT * 0.1),
                  self.st.nodes[alt][0].animate.set_stroke(color=CYAN), FadeOut(self.st.lit[0]),
                  run_time=0.5)
        self.remove(old)
        self.st.user.q_box = None
        self.play(*self.st.code.reset(), run_time=0.2)
        # the director's question, with no zone: the harness has to derive it from their rights
        self.st.question = self.st.user.type_question(self, tr(QUESTION_ME))
        self.ask_format()
        frame, title, grid, box = self.st.strip
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
        self.play(*self.st.code.step(1), run_time=0.25)
        # with the descriptions, the AI picks the right tool straight away
        scan = SurroundingRectangle(VGroup(grid[SEL], descs[SEL]), color=ORANGE, buff=0.03, corner_radius=0.05,
                                    stroke_width=1.6).set_z_index(8)
        self.play(Create(scan), run_time=0.3)
        # "parking sessions" = off-street by default: the context matches, the right tool is picked
        self.play(descs[SEL].animate.set_color(ORANGE), grid[SEL][0].animate.set_stroke(ORANGE, 2, 1),
                  Flash(grid[SEL], color=ORANGE, flash_radius=0.6, num_lines=10),
                  run_time=0.5)
        self.st.descs = VGroup(descs, scan)

    def b_scoped_call(self):
        descs, scan = self.st.descs
        self.play(FadeOut(VGroup(descs, scan)), descs[SEL].animate.set_color(GREY_B), run_time=0.4)
        self.run(CALL_OK, ("09:14 sessions · west OK", GREEN), to_chat=True, ask=False, scope=self.st.badge)
        right = self.chat_reply(tr("0.31 M"), tr("OFF-STREET · WEST ZONE · 09/26"), color=GREEN)
        self.st.ok = icon_check(GREEN, 0.5).next_to(right, RIGHT, 0.15).set_z_index(6)
        self.play(FadeIn(right, shift=UP * 0.1), Create(self.st.ok), Flash(right, color=GREEN, flash_radius=1.0),
                  FadeIn(self.st.lit_ok.set_stroke(CYAN, opacity=1)), run_time=0.6)
        self.st.reply = right

    def b_condense(self):
        """Everything is explained: the detail condenses into icons (big picture)."""
        self.hold(0.8)   # the demonstration is done
        self.play(*self.reset_gates(), FadeOut(self.st.lit_ok), run_time=0.4)
        chip, old = self.st.chip, self.st.box_shape
        log_m = Module(icon_log(ORANGE), [chip.get_right()[0] + 0.6, OUT_Y, 0])
        left, right = old.get_left()[0], log_m.get_right()[0] + 0.4
        top, bottom = chip.get_top()[1] + 0.65, old.get_bottom()[1]   # no more TOOLS step in the frame
        box = RoundedRectangle(corner_radius=0.18, width=right - left, height=top - bottom)
        box.move_to([(left + right) / 2, (top + bottom) / 2, 0])
        tag = VGroup(icon_doc(ORANGE).scale(0.45), T_("harness.py", font=MONO, font_size=10, color=ORANGE))
        tag.arrange(RIGHT, buff=0.08).next_to(box, UP, 0.1).align_to(box, LEFT)
        label = self.st.frame_label
        lbl_t = label.copy().scale(0.75).move_to([box.get_x(), box.get_top()[1] - 0.28, 0])   # inside the frame
        tests_t = self.st.tests.copy().next_to(tag, RIGHT, 0.2)
        self.st.code[1].clear_updaters()
        # semantic layer: the 5 domains → one icon, the 10 tables → one database
        mid = (left + right) / 2
        band = RoundedRectangle(corner_radius=0.12, width=right - left, height=0.9).move_to([mid, BAND_Y, 0])
        mcp_lbl = self.st.band_label.copy().move_to(band)
        # the data: one plain big rectangle
        db_box, db = data_block(right - left, [mid, DATA_Y, 0], tr("DATA"))
        trunk = rail([chip.port(DOWN), [chip.port(DOWN)[0], band.get_top()[1], 0]], CYAN, 2).set_stroke(opacity=0.5)
        link = rail([band.get_bottom(), db.get_top() + UP * 0.05], CYAN, 1.6).set_stroke(opacity=0.5)
        R_ = box.get_right()[0]
        self.play(Transform(self.st.frame, neon(box, ORANGE, 2)), self.st.clamps[1].animate.move_to([R_, OUT_Y, 0]),
                  FadeOut(VGroup(self.st.strip[0], self.st.strip[1], self.st.strip[2])),
                  FadeTransform(VGroup(self.st.gates[3], self.st.logs), log_m), FadeOut(self.st.scope_pill),
                  FadeOut(self.st.code, scale=0.4, target_position=tag), FadeIn(tag, scale=1.6), Transform(label, lbl_t),
                  Transform(self.st.tests, tests_t),
                  Transform(self.st.band, neon(band, CYAN, 2, fill=ManimColor("#021B21"))),
                  FadeOut(self.st.nodes), Transform(self.st.band_label, mcp_lbl), FadeOut(self.st.sens_lbl),
                  FadeOut(self.st.bus), FadeOut(self.st.roots), Transform(self.st.trunk, trunk),
                  ReplacementTransform(self.st.tables[0], db), FadeIn(link), run_time=1.6)
        self.st.gates.submobjects[3] = log_m
        self.st.box_shape, self.st.band_shape = box, band
        self.st.bus, self.st.roots, self.st.nodes, self.st.tables = VGroup(), VGroup(link), VGroup(), VGroup(db)
        self.st.tools_icon, self.st.tag, self.st.condensed = VGroup(), tag, True

    # =============================================================================================================
    # 06 · Together: chat → harness → MCP → data; the answer becomes tables, charts, reports; end on words
    # =============================================================================================================
    def b_big_picture(self):
        self.chapter("06 · TOGETHER", "Together")
        box, band = self.st.box_shape, self.st.band_shape
        # the harness is explained: no more detail inside, only the frame around the AI
        self.play(FadeOut(VGroup(self.st.gates, self.st.tools_icon, self.st.tag, self.st.tests)), run_time=0.6)
        # the whole circuit lights up once, then the two key ideas flash next to their block
        self.play(flash_along(self.st.in_rail, WHITE, 5, run_time=0.9), flash_along(self.st.trunk, WHITE, 5, run_time=0.9),
                  *[flash_along(r, WHITE, 5, run_time=0.9) for r in self.st.roots], self.st.chip.pulse(), run_time=0.9)
        self.play(flash_along(box, ORANGE, 6, time_width=0.4, run_time=0.8),
                  flash_along(band, CYAN, 6, time_width=0.4, run_time=0.8), run_time=0.8)

    def b_deliverables(self):
        # on the right: the answer turns into deliverables
        box = self.st.box_shape
        bars = VGroup(*[Rectangle(width=0.1, height=h).set_fill(GREEN, 0.8).set_stroke(width=0)
                        for h in (0.18, 0.32, 0.24, 0.42)]).arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
        outs = VGroup()
        for icon, name in [(icon_sheet(GREEN), "TABLES"), (bars, "CHARTS"), (icon_doc(GREEN), "REPORTS")]:
            outs.add(VGroup(icon, L(name, 9, GREEN, spacing=3)).arrange(DOWN, buff=0.15))
        outs.arrange(RIGHT, buff=0.5).move_to([(box.get_right()[0] + FW / 2) / 2 + 0.2, OUT_Y + 0.3, 0])
        self.play(self.st.reply.animate.shift(UP * 0.04), self.st.ok.animate.shift(UP * 0.04), run_time=0.2)
        src = self.st.reply.copy()
        self.play(src.animate.move_to(outs).scale(0.8), run_time=0.7)
        self.play(FadeOut(src, scale=0.6), LaggedStart(*[FadeIn(o, scale=0.8) for o in outs], lag_ratio=0.2),
                  run_time=0.9)
        self.st.outs = outs

    def b_back_to_user(self):
        # sent back to the user, in all these forms: they arrive in the chat
        back = VGroup(*[o[0].copy() for o in self.st.outs])
        dest = back.copy().scale(0.45).arrange(RIGHT, buff=0.22)
        dest.next_to(self.st.reply, DOWN, 0.06).align_to(self.st.reply, LEFT).set_z_index(6)
        back.set_z_index(6)
        self.play(LaggedStart(*[b.animate(path_arc=PI / 5).move_to(d).scale(0.45) for b, d in zip(back, dest)],
                              lag_ratio=0.15), flash_along(self.st.in_rail, GREEN, 5, run_time=1.0), run_time=1.1)
        self.play(Flash(self.st.user[0], color=GREEN, flash_radius=1.9, num_lines=14), run_time=0.7)

    def b_trust_meaning(self):
        # last shot: the rectangles disappear and become the words that sum up the film
        w1 = L("TRUST", 26, ORANGE, spacing=10)
        w2 = L("SEMANTIC LAYER", 26, CYAN, spacing=10)
        w3 = L("RETRIEVING DYNAMIC DATA", 20, WHITE, spacing=8)
        VGroup(w1, w2, w3).arrange(DOWN, buff=0.55).move_to([0, 0.2, 0])
        harness = VGroup(self.st.frame, self.st.frame_label, self.st.clamps)
        mcp = VGroup(self.st.band, self.st.band_label)
        data = self.st.tables
        keep = {id(m) for g in (harness, mcp, data) for m in g.get_family()} | {id(self.chapter_lbl)}
        rest = [m for m in self.mobjects if id(m) not in keep and m is not self.chapter_lbl]
        self.play(*[FadeOut(m) for m in rest], run_time=0.7)
        # the three blocks re-centre, then turn into words
        # the harness becomes TRUST; the MCP becomes SEMANTIC LAYER, then UNDERSTANDING
        words_from_blocks(self, [(harness, w1), (mcp, w2)], fade=[data], center=[0, 0.2, 0])
        self.st.words = VGroup(w1, w2, w3)

    def b_understanding(self):
        w1, w2, w3 = self.st.words
        und = L("UNDERSTANDING", 26, CYAN, spacing=10).move_to(w2)
        self.play(FadeTransform(w2, und), run_time=0.9)

    def b_retrieving(self):
        # and finally, underneath: retrieving dynamic data
        self.play(FadeIn(self.st.words[2], shift=UP * 0.12), run_time=0.9)
