"""Actors: recurring characters built from primitives (chip, chat, badge, panels, band, data, code file, harness).

Actors take display-ready text (already translated by the film). Parts are named attributes; submobject order
is part of the look (it is the drawing order), so keep it when extending an actor.
Never assign `self.color` / `self.fill_opacity`… on an actor: Manim treats them as setters and recolours the group.
"""

import numpy as np
from manim import *

from .primitives import BODY, CYAN, DIMC, GREEN, ICE, MONO, NEON_OPS, ORANGE, TITLE, label, neon


# --- The chip ---------------------------------------------------------------------------------------
class Chip(VGroup):
    def __init__(self, size=1.5, color=ICE, label_text="AI"):
        super().__init__()
        self.size, self.color = size, color
        body = RoundedRectangle(corner_radius=0.12, width=size, height=size)
        die = RoundedRectangle(corner_radius=0.06, width=size * 0.56, height=size * 0.56)
        pins = VGroup()
        for d in (UP, DOWN, LEFT, RIGHT):
            n = d[[1, 0, 2]] * np.array([1, 1, 0])  # direction along the side
            for k in range(-2, 3):
                base = d * size / 2 + n * k * size * 0.17
                pins.add(Line(base, base + d * 0.16))
        wires = VGroup(*[Line(die.get_corner(v), body.get_corner(v) - v * 0.18) for v in (UL, UR, DL, DR)])
        self.body = neon(body, color, 2.5, fill=BODY)
        self.die = neon(die, color, 1.5)
        self.pins = neon(pins, color, 2)
        self.wires = wires.set_stroke(color, 1.2, opacity=0.6)
        self.label = label(label_text, int(size * 17), color, spacing=3).move_to(body)
        self.add(self.pins, self.body, self.wires, self.die, self.label)

    def pulse(self, color=WHITE):
        edge = self.body[1].copy().set_fill(opacity=0)
        return ShowPassingFlash(edge.set_stroke(color, 6), time_width=0.5, run_time=1.0)

    def port(self, d):
        """Tip of the middle pin on side d (where rails connect)."""
        return self.body.get_center() + d * (self.size / 2 + 0.16)

    # pins: hidden until something connects to them
    PIN_SIDES = {"UP": 0, "DOWN": 1, "LEFT": 2, "RIGHT": 3}

    def pin_parts(self, side, k):
        i = self.PIN_SIDES[side] * 5 + (k + 2)
        return [g[i] for g in self.pins[0]] + [self.pins[1][i]]

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
            for part, op in zip(self.pin_parts(side, k), NEON_OPS):
                anims.append(part.animate.set_stroke(opacity=op))
        return anims

    def pin(self, k):
        """Tip of the k-th bottom pin (k = -2 … 2, 0 = centre)."""
        return self.body.get_center() + np.array([-k * self.size * 0.17, -(self.size / 2 + 0.16), 0])


# --- Packet ------------------------------------------------------------------------------------------
def packet(color=ICE):
    """Data packet: a bright square in a soft halo (travels along rails with motions.send)."""
    p = VGroup(Square(0.12).set_fill(color, 1).set_stroke(width=0),
               Square(0.24).set_fill(color, 0.15).set_stroke(width=0))
    return p.set_z_index(8)


# --- Chat (the user) ---------------------------------------------------------------------------------
class Chat(VGroup):
    """Chat window standing for the user: questions typed on the right, answers on the left.
    Parts: [0] neon window, [1] header line, [2] title. `win` is the window shape."""

    def __init__(self, center, width=3.4, height=1.9, title="CHAT · AI"):
        win = RoundedRectangle(corner_radius=0.14, width=width, height=height).move_to(center)
        head = Line(win.get_corner(UL) + DOWN * 0.38, win.get_corner(UR) + DOWN * 0.38).set_stroke(DIMC, 1)
        ttl = VGroup(Circle(0.05).set_fill(ORANGE, 1).set_stroke(width=0), label(title, 9, GREY_B, spacing=4))
        ttl.arrange(RIGHT, buff=0.12).move_to(win.get_corner(UL) + np.array([0.22, -0.19, 0]), aligned_edge=LEFT)
        super().__init__(neon(win, ICE, 1.6, fill=BODY), head, ttl)
        self.set_z_index(3)
        self.win, self.q_box = win, None

    def bubble_pos(self):
        return self.win.get_corner(UR) + np.array([-0.2, -0.62, 0])

    @staticmethod
    def bubble(text):
        """Question bubble (right side of the chat), text ready to be typed."""
        txt = label(text, 10, ICE, spacing=2)
        box = RoundedRectangle(corner_radius=0.1, width=txt.width + 0.36, height=txt.height + 0.24)
        box.set_fill(ManimColor("#0B2730"), 1).set_stroke(width=0)
        return VGroup(box, txt.move_to(box)).set_z_index(4)

    def type_question(self, scene, text):
        """The question is typed in a bubble (replacing the previous one). Returns the text mobject."""
        txt = label(text, 10, ICE, spacing=2)
        box = RoundedRectangle(corner_radius=0.1, width=txt.width + 0.36, height=txt.height + 0.24)
        box.set_fill(ManimColor("#0B2730"), 1).set_stroke(width=0)
        VGroup(box, txt.move_to(box)).move_to(self.bubble_pos(), aligned_edge=UR).set_z_index(4)
        anims = [FadeIn(box, shift=LEFT * 0.1)]
        if self.q_box is not None:
            anims.append(FadeOut(self.q_box))
        scene.play(*anims, run_time=0.3)
        with scene.exact():
            scene.play(AddTextLetterByLetter(txt, time_per_char=0.02), run_time=0.5)
        self.q_box = box
        return txt

    def reply(self, main, sub, color=CYAN):
        """AI answer, left-aligned below the question: a big value + a small caption."""
        txt = VGroup(Text(main, font=TITLE, font_size=20, color=color), label(sub, 7, color, spacing=1))
        txt.arrange(DOWN, buff=0.06, aligned_edge=LEFT)
        box = RoundedRectangle(corner_radius=0.1, width=txt.width + 0.36, height=txt.height + 0.24)
        box.set_fill(BODY, 1).set_stroke(color, 1.2, 0.9)
        pos = self.win.get_corner(UL) + np.array([0.2, -1.0, 0])
        return VGroup(box, txt.move_to(box)).move_to(pos, aligned_edge=UL).set_z_index(4)


class Badge(VGroup):
    """User identity under the chat: pictogram + context text. Parts: [0] pictogram, [1] text, [2] background."""

    def __init__(self, text, under):
        head = Circle(0.055).set_stroke(ICE, 1.4)
        body = Arc(radius=0.11, start_angle=0, angle=PI).set_stroke(ICE, 1.4)
        icon = VGroup(head, body.next_to(head, DOWN, 0.02).flip(RIGHT))
        row = VGroup(icon, self.text(text)).arrange(RIGHT, buff=0.14)
        bg = BackgroundRectangle(row, color=BLACK, fill_opacity=1, buff=0.06)
        row.add_to_back(bg)
        super().__init__(icon, row[2], bg)
        self.next_to(under, DOWN, 0.16).align_to(under, LEFT).shift(RIGHT * 0.1)
        icon.set_z_index(5)
        self[1].set_z_index(5)
        bg.set_z_index(3)

    @staticmethod
    def text(text):
        return label(text, 9, ICE, spacing=3)

    def grow(self, text, color=ICE):
        """The context gains an item (the new text lights up in `color`)."""
        new = self.text(text).set_color(color).next_to(self[0], RIGHT, 0.14).set_z_index(5)
        bg = BackgroundRectangle(VGroup(self[0], new), color=BLACK, fill_opacity=1, buff=0.06).set_z_index(3)
        return [Transform(self[1], new), Transform(self[2], bg)]


# --- Panels, band, data ----------------------------------------------------------------------------
def panel_frame(left, y, text, icon, color, w=2.7, h=2.9):
    """Side panel explaining the mechanism. Returns (shape, neon frame, title)."""
    box = RoundedRectangle(corner_radius=0.12, width=w, height=h).move_to([left + w / 2, y, 0])
    frame = neon(box, color, 1.6, fill=BODY)
    title = VGroup(icon, label(text, 9, color, spacing=4))
    title.arrange(RIGHT, buff=0.12).move_to(box.get_corner(UL) + np.array([0.18, -0.24, 0]), aligned_edge=LEFT)
    return box, frame, title.set_z_index(3)


class Band(VGroup):
    """A wide layer (e.g. the MCP / semantic layer): shape, neon frame, title block on the left.
    Not added to the scene by itself: add `frame` and `label` when needed."""

    def __init__(self, width, height, center, title, subtitle, color=CYAN, fill=ManimColor("#021B21")):
        super().__init__()
        self.shape = RoundedRectangle(corner_radius=0.12, width=width, height=height).move_to(center)
        self.accent, self.fill_color = color, fill
        self.label = VGroup(label(title, 20, color, spacing=6), label(subtitle, 8, color, spacing=1))
        self.label.arrange(DOWN, buff=0.06)

    def frame(self, color=None, fill=None):
        return neon(self.shape, color or self.accent, 2, fill=fill or self.fill_color)


def data_block(width, center, text, color=CYAN, height=0.8):
    """The data, condensed: one big rectangle with a word. Returns (shape, group)."""
    box = RoundedRectangle(corner_radius=0.12, width=width, height=height).move_to(center)
    return box, VGroup(neon(box, color, 1.6, fill=BODY), label(text, 12, color, spacing=6).move_to(box))


# --- Harness -----------------------------------------------------------------------------------------
class Module(VGroup):
    """A harness step: square with an icon, optional label. Parts: [0] frame, [1] icon, [2] label, [3] spare."""

    def __init__(self, icon, pos, name=None, side=DOWN, color=ORANGE):
        sq = RoundedRectangle(corner_radius=0.06, width=0.6, height=0.6).move_to(pos)
        lbl = label(name, 8, color, spacing=2).next_to(sq, side, 0.1) if name else VGroup()
        super().__init__(neon(sq, color, 1.6, fill=BODY), icon.scale(0.85).move_to(sq), lbl, VGroup())


def harness_frame(box, color=ORANGE):
    return neon(box, color, 2)


def harness_clamps(box, io_y, data_x, color=ORANGE):
    """The harness locks: input (left), output (right) and data access (bottom)."""
    l, r, b = box.get_left()[0], box.get_right()[0], box.get_bottom()[1]
    return VGroup(
        RoundedRectangle(corner_radius=0.03, width=0.12, height=0.46).move_to([l, io_y, 0]),
        RoundedRectangle(corner_radius=0.03, width=0.12, height=0.46).move_to([r, io_y, 0]),
        RoundedRectangle(corner_radius=0.03, width=0.46, height=0.12).move_to([data_x, b, 0]),
    ).set_fill(color, 1).set_stroke(width=0)


class CodeFile(VGroup):
    """A code file that runs: scrolling binary behind, instructions lighting up as they execute.
    Parts: [0] frame, [1] binary, [2] header, [3] line backgrounds, [4] lines, [5] cursor."""

    def __init__(self, left, right, y, lines, name="harness.py", h=2.7, seed=11, color=ORANGE):
        w = right - left
        box = RoundedRectangle(corner_radius=0.1, width=w, height=h).move_to([left + w / 2, y, 0])
        frame = neon(box, color, 1.4, fill=BODY)
        head = Text(name, font=MONO, font_size=11, color=color)
        head.move_to(box.get_corner(UL) + np.array([0.16, -0.18, 0]), aligned_edge=UL)
        rng = np.random.default_rng(seed)
        y_top, y_bot = box.get_top()[1] - 0.42, box.get_bottom()[1] + 0.12
        n = 12
        step = (y_top - y_bot) / n
        binary = VGroup(*[Text(" ".join(str(int(b)) for b in rng.integers(0, 2, 26)), font=MONO, font_size=7,
                               color=color).set_opacity(0.16) for _ in range(n)])
        for i, r in enumerate(binary):
            r.move_to([box.get_x(), y_top - i * step, 0])

        def scroll(m, dt):  # the binary scrolls up in a loop
            for r in m:
                r.shift(UP * dt * 0.35)
                if r.get_y() > y_top:
                    r.shift(DOWN * step * n)
        binary.add_updater(scroll)
        code = VGroup(*[Text(t, font=MONO, font_size=10, color=ICE) for t in lines])
        code.arrange(DOWN, buff=0.17, aligned_edge=LEFT)
        code.move_to(box.get_corner(UL) + np.array([0.38, -0.5, 0]), aligned_edge=UL)
        bgs = VGroup(*[BackgroundRectangle(l_, color=BODY, fill_opacity=0.85, buff=0.03) for l_ in code])
        cursor = Text("▸", font=MONO, font_size=10, color=color).next_to(code[0], LEFT, 0.1).set_opacity(0)
        super().__init__(frame, binary, head, bgs, code, cursor)
        self.lines, self.cursor, self.on, self.accent = code, cursor, None, color

    def step(self, i):
        """Line i runs: it lights up, the previous one turns green."""
        anims = []
        if self.on is not None and self.on != i:
            anims.append(self.lines[self.on].animate.set_color(GREEN))
        anims += [self.lines[i].animate.set_color(self.accent),
                  self.cursor.animate.set_opacity(1).next_to(self.lines[i], LEFT, 0.1)]
        self.on = i
        return anims

    def reset(self):
        self.on = None
        return [*[l_.animate.set_color(ICE) for l_ in self.lines], self.cursor.animate.set_opacity(0)]
