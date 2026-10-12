"""Actors: recurring characters built from primitives (chip, chat, badge, panels, band, data, code file, harness)."""

import numpy as np
from manim import *

from .primitives import BODY, ICE, label, neon


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
        return self.body.get_center() + d * (self.size / 2 + 0.16)


# --- Packet ------------------------------------------------------------------------------------------
def packet(color=ICE):
    """Data packet: a bright square in a soft halo (travels along rails with motions.send)."""
    p = VGroup(Square(0.12).set_fill(color, 1).set_stroke(width=0),
               Square(0.24).set_fill(color, 0.15).set_stroke(width=0))
    return p.set_z_index(8)
