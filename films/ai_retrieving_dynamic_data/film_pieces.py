"""Film-specific building blocks used by the beats: map, wiring and tree, panels, the harness run, condense.

A mixin of the Film scene (methods use self.play and self.st, the Stage).
"""

import numpy as np
from manim import *

from studio.kit import primitives as kit
from studio.kit.actors import (Badge, Band, Chat, Chip, CodeFile, Module, data_block, harness_clamps, harness_frame,
                               packet, panel_frame)
from studio.kit.i18n import Translator, current_lang
from studio.kit.layout import (ANS_IN, BAND_Y, BUS_Y, CHAT_C, CHAT_H, CHAT_W, CHIP_POS, DATA_Y, IN_X,
                               OUT_Y, USER_POS)
from studio.kit.motions import dim, morph, send, words_from_blocks
from studio.kit.primitives import (BODY, CYAN, DIMC, GREEN, ICE, LABEL, MONO, NEON_OPS, ORANGE, RED, TITLE, flash_along,
                                   globe, icon_check, icon_doc, icon_format, icon_list, icon_lock, icon_log, icon_mail,
                                   icon_scope, icon_sheet, icon_tool_card, icon_user, neon, rack, rail, square_dot)

from film_data import *  # noqa: F401,F403  (text, business data, layout)


class Pieces:
    def ask(self, color=ICE, run_time=0.6):
        p = packet(color)
        send(self, p, [[IN_X, OUT_Y, 0], self.st.chip.port(LEFT)], color, run_time=run_time)
        self.play(self.st.chip.pulse(), FadeOut(p), run_time=0.45)

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
        new = self.st.racks[self.st.racks_on:n]
        anims = []
        if k > 0:
            ev, st = self.mag_events(k), self.mag_storage(k)
            anims += [FadeTransform(self.st.ev_count, ev), FadeTransform(self.st.st_count, st)]
            self.st.ev_count, self.st.st_count = ev, st
        if len(new):
            anims.append(LaggedStart(*[FadeIn(r, shift=UP * 0.1) for r in new], lag_ratio=0.15))
            anims.append(LaggedStart(*[AnimationGroup(r[0].animate.set_stroke(color=CYAN), r[1].animate.set_stroke(ICE),
                                                      LaggedStart(*[l.animate.set_fill(GREEN, 1) for l in r[2]],
                                                                  lag_ratio=0.2))
                                       for r in new], lag_ratio=0.2))
        self.st.racks_on = n
        return anims

    def to_servers(self, sources, n=24, seed=0):
        """While zooming out, data packets leave the map and rush to the lit racks."""
        rng = np.random.default_rng(seed)
        racks = [r for r in self.st.racks[:self.st.racks_on]] or [self.st.racks[0]]
        pk = []
        for k in range(n):
            src = sources[int(rng.integers(0, len(sources)))]
            r = racks[int(rng.integers(0, len(racks)))]
            d = packet(CYAN).scale(0.55).move_to(src.get_center())
            pk.append((d, r[2][int(rng.integers(0, 6))].get_center()))
        self.add(*[d for d, _ in pk])
        return [LaggedStart(*[d.animate(rate_func=rate_functions.ease_in_out_sine).move_to(t).scale(0.4)
                              .set_opacity(0) for d, t in pk], lag_ratio=0.03),
                LaggedStart(*[Indicate(r[2], color=WHITE, scale_factor=1.0) for r in racks], lag_ratio=0.1)]

    def set_level(self, k):
        new_lbl = L(LEVELS[k], 18, GREY_B, spacing=10).scale(PV_K).move_to(self.st.level_lbl)
        count = self.mag_count(k)
        anims = [FadeTransform(self.st.level_lbl, new_lbl), FadeTransform(self.st.count, count), *self.fill_racks(k)]
        self.st.level_lbl, self.st.count = new_lbl, count
        return anims

    def build_wiring(self):
        """Red rails leaving the pins and branching like the tree of definitions."""
        red = lambda pts: rail(pts, RED, 1.6).set_stroke(opacity=0.75)
        self.st.seg1, self.st.seg2, self.st.seg3, self.st.cut_pts = VGroup(), VGroup(), [], []
        self.st.j1_pos, self.st.j2_pos = [], []
        for i, (pin_k, yb) in enumerate([(1, -0.38), (-1, -0.52)]):
            p, j1 = self.st.chip.pin(pin_k), J1_POS[i]
            self.st.seg1.add(red([p, [p[0], yb, 0], [j1[0], yb, 0], j1 + UP * 0.16]))
            self.st.j1_pos.append(j1)
            for j in range(2):
                leaf = 2 * i + j
                j2 = np.array([j1[0] + (j - 0.5) * 2 * J2_DX, J2_Y, 0])
                self.st.j2_pos.append(j2)
                self.st.seg2.add(red([j1 + DOWN * 0.16, [j1[0], j1[1] - 0.38, 0], [j2[0], j1[1] - 0.38, 0],
                                   j2 + UP * 0.25]))
                lines = VGroup()
                for n, ti in enumerate(LEAF_TABLES[leaf]):
                    t = self.st.tables[ti]
                    y = -2.35 - 0.12 * ((leaf * 3 + n) % 5)
                    x0 = j2[0] + (n - (len(LEAF_TABLES[leaf]) - 1) / 2) * 0.12
                    lines.add(red([[x0, J2_Y - 0.25, 0], [x0, y, 0], [t.get_x(), y, 0], t.get_top()]))
                    self.st.cut_pts.append(np.array([t.get_x(), (y + t.get_top()[1]) / 2, 0]))
                self.st.seg3.append(lines)
        self.st.chaos = VGroup(*self.st.seg1, *self.st.seg2, *self.st.seg3)
        self.st.joints = VGroup(*[Square(0.12).set_fill(RED, 1).set_stroke(width=0).move_to(p)
                               for p in self.st.j1_pos + self.st.j2_pos])

    def build_tree(self):
        """The wiring junctions become the tree nodes (same positions)."""
        nodes1, nodes2, leaves = VGroup(), VGroup(), VGroup()
        for i, name in enumerate(TREE_L1):
            lbl = L(name, 10, ICE, spacing=2)
            box = RoundedRectangle(corner_radius=0.05, width=lbl.width + 0.3, height=0.32).move_to(self.st.j1_pos[i])
            nodes1.add(VGroup(neon(box, DIMC, 1.1, fill=BODY), lbl.move_to(box)))
            for j, name2 in enumerate(TREE_L2):
                leaf = 2 * i + j
                lbl2 = VGroup(L(name2, 8, ICE, spacing=2), Text(TREE_LEAVES[leaf], font=TITLE, font_size=14,
                                                                color=GREY_B)).arrange(DOWN, buff=0.05)
                box2 = RoundedRectangle(corner_radius=0.05, width=1.2, height=0.5).move_to(self.st.j2_pos[leaf])
                nodes2.add(VGroup(neon(box2, DIMC, 1.1, fill=BODY), lbl2.move_to(box2)))
                leaves.add(lbl2[1])
        return nodes1, nodes2, leaves

    def node_style(self, n, color, f, animate=True):
        """Colour + intensity of a tree node (neon halo, stroke, fill, text), without flattening the halos."""
        glow, core = n[0]
        targets = [(g, dict(color=color, opacity=NEON_OPS[j] * f)) for j, g in enumerate(glow)]
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
        n1, n2, lv = self.st.tree
        dim = [m.animate.set_stroke(RED, 1.6 * 0.65, BOTTOM_DIM) for m in self.st.chaos] + \
              [a for n in (*n1, *n2) for a in self.node_style(n, DIMC, BOTTOM_DIM)] + \
              [l.animate.set_color(GREY_B).set_opacity(TEXT_DIM) for l in lv] + \
              [t[0].animate.set_stroke(DIMC) for t in self.st.tables]
        lit = [self.st.seg1[i].animate.set_stroke(color, 2.4, 1), self.st.seg2[leaf].animate.set_stroke(color, 2.4, 1),
               *[m.animate.set_stroke(color, 2.4, 1) for m in self.st.seg3[leaf]],
               *self.node_style(n1[i], color, 1), *self.node_style(n2[leaf], color, 1),
               lv[leaf].animate.set_color(color).set_opacity(1),
               *[self.st.tables[ti][0].animate.set_stroke(color, 2) for ti in LEAF_TABLES[leaf]]]
        return dim, lit

    def llm_sends(self, chip_m, target, color):
        """The AI sends its choice: the pill leaves the chip, follows the line to the panel and lands."""
        fly = chip_m.copy().scale(0.85)
        x_in = ANS_IN[0] + 0.12
        route = [self.st.chip.port(RIGHT), [x_in, OUT_Y, 0], [x_in, target.get_y(), 0], target.get_left() + LEFT * 0.05]
        send(self, fly, route, color, run_time=0.8)
        self.play(fly.animate.scale(1 / 0.85).move_to(target), run_time=0.25)
        self.remove(fly)
        self.add(target)

    def panel_frame(self, text, icon, color, h=2.9):
        """Shared frame of the right-hand panels (act 03: no map · act 04: tool call · act 05: tools)."""
        return panel_frame(ANS_IN[0], OUT_Y - 0.4, tr(text), icon, color, h=h)

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
        self.st.p3_box = box
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
        return call.move_to(self.st.p3_box.get_bottom() + UP * 0.38).set_z_index(3)

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
        w, h = self.st.box_shape.width - 0.3, TOOLS_H
        box = RoundedRectangle(corner_radius=0.12, width=w, height=h)
        box.move_to([self.st.box_shape.get_x(), self.st.chip.get_top()[1] + 0.12 + h / 2, 0])
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
        return self.st.user.reply(main, tr(sub), color)

    def badge_text(self, k):
        return " · ".join(tr(x) for x in USER_CTX[k])

    def add_log(self, text, color):
        if self.st.condensed:  # the audit log becomes just an icon
            return Wait(0.01)
        entry = T_(text, font=MONO, font_size=11, color=color)
        entry.move_to(self.st.log_top + DOWN * 0.25 * len(self.st.logs), aligned_edge=UL)
        self.st.logs.add(entry)
        return FadeIn(entry, shift=UP * 0.1)

    def gate_state(self, g, color):
        return [g[0].animate.set_stroke(color=color), g[1].animate.set_color(color)]

    def reset_gates(self):
        return [a for g in self.st.gates for a in self.gate_state(g, ORANGE)]

    def check(self, k, ok=True):
        """A module runs: its own visual effect + colour."""
        g = self.st.gates[k]
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
        anims = self.st.code.step(GATE_LINE[k]) if self.st.code is not None else []
        return [*self.gate_state(g, GREEN if ok else RED), *fx, *anims]

    def ask_format(self):
        """The question enters the harness: FORMAT checks it before it reaches the chip."""
        p = packet(ICE)
        g0 = self.st.gates[0][0].get_center()
        send(self, p, [[IN_X, OUT_Y, 0], g0], ICE, run_time=0.35)
        self.play(*self.check(0), run_time=0.35)
        send(self, p, [g0, self.st.chip.port(LEFT)], GREEN, run_time=0.3)
        self.play(self.st.chip.pulse(), FadeOut(p), run_time=0.4)

    def run(self, call_text, log, to_chat=False, ask=True, scope=None):
        """Question → chip → checked tool call → MCP → chip → checked answer → user."""
        if ask:
            self.ask_format()
            self.play(*self.st.code.step(1), Flash(self.st.strip[2][SEL], color=ORANGE, flash_radius=0.5), run_time=0.35)
        p = packet(CYAN)
        top = self.st.chip.port(DOWN)
        g1, g2 = self.st.gates[1][0].get_center(), self.st.gates[2][0].get_center()
        send(self, p, [top, g1], CYAN, run_time=0.3)
        if scope is not None:  # SCOPE does not know the zone: it calls the user's rights
            self.scope_lookup(scope)
        self.play(*self.check(1), run_time=0.35)
        send(self, p, [g1, g2], CYAN, run_time=0.3)
        self.play(*self.check(2), run_time=0.3)
        node = self.st.nodes[SEL]
        path = [g2, [CHIP_POS[0], BUS_Y, 0]] + self.st.bus_pts[SEL][1:]
        # the call reaches the MCP: the semantic layer lights up (the rails stay subtle)
        paths = [self.st.bus, self.st.trunk, self.st.lit, self.st.roots]
        rest = [m for m in self.st.background if all(m is not p_ for p_ in paths)]
        self.play(dim(rest, 1.0), dim(paths, 0.45), *self.st.code.step(4), run_time=0.35)
        send(self, p, path, CYAN, run_time=0.6)
        self.play(Flash(node, color=CYAN, flash_radius=0.8), run_time=0.35)
        # the MCP fetches the data, then goes back up
        down = [node.get_bottom(), [node.get_x(), self.st.data_box.get_top()[1], 0]]
        send(self, p, down, CYAN, run_time=0.35)
        self.play(Flash(p, color=CYAN, flash_radius=0.5, num_lines=8), run_time=0.3)
        send(self, p, list(reversed(down)), CYAN, run_time=0.35)
        send(self, p, list(reversed(path)) + [top], CYAN, run_time=0.7)
        self.play(self.st.chip.pulse(CYAN), run_time=0.35)
        g3 = self.st.gates[3][0].get_center()
        send(self, p, [self.st.chip.port(RIGHT), g3], GREEN, run_time=0.4)
        self.play(*self.check(3), self.add_log(*log), run_time=0.35)
        if not to_chat:
            send(self, p, [g3, ANS_IN], GREEN, run_time=0.35)
        self.play(FadeOut(p, scale=0.3), run_time=0.15)

    def scope_lookup(self, badge):
        """SCOPE calls for the user's scope; the zone comes back and attaches to the module."""
        g = self.st.gates[1][0]
        x = (self.st.box_shape.get_left()[0] + self.st.user.win.get_right()[0]) / 2
        route = [g.get_left(), [x, g.get_y(), 0], [x, badge.get_y(), 0], badge.get_right() + RIGHT * 0.08]
        q = packet(ORANGE)
        send(self, q, route, ORANGE, run_time=0.6)
        self.play(FadeOut(q), Flash(badge[0], color=ORANGE, flash_radius=0.35, num_lines=8),
                  *self.st.badge.grow(self.badge_text(2)), run_time=0.5)
        txt = L("WEST ZONE", 8, ORANGE, spacing=2)
        box = RoundedRectangle(corner_radius=0.06, width=txt.width + 0.22, height=0.24)
        pill = VGroup(box.set_fill(BODY, 1).set_stroke(ORANGE, 1.2, 1), txt.move_to(box)).set_z_index(8)
        dest = g.get_right() + RIGHT * (0.2 + pill.width / 2)
        send(self, pill, list(reversed(route)) + [dest], ORANGE, run_time=0.8)
        self.st.scope_pill = pill
