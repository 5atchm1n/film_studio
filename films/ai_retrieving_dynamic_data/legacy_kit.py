"""Briques visuelles TRON du film : couleurs, polices, néon, pistes, icônes, puce.

Extrait de tron.py (génération 2) : seules les pièces réellement utilisées par film.py,
avec les réglages « affinés » du film (néon fin, pistes à 65 % de l'épaisseur nominale).
Aucune dépendance à manim-slides, story.py ou presentation.py.
"""

import numpy as np
from manim import *

config.background_color = "#000000"

# --- Couleurs ------------------------------------------------------------------------------------
CYAN = ManimColor("#00E5FF")      # MCP · le sens
ICE = ManimColor("#CFF8FF")       # IA, textes
ORANGE = ManimColor("#FF9E1B")    # Harness · la confiance
RED = ManimColor("#FF3355")       # erreur, refus
GREEN = ManimColor("#2BFF88")     # validé
DIMC = ManimColor("#1D3A44")      # pistes éteintes
BODY = ManimColor("#020A0F")      # fond des blocs

# --- Polices --------------------------------------------------------------------------------------
LABEL = "DIN Alternate"
TITLE = "Futura"
MONO = "Menlo"


def label(text, size=20, color=ICE, spacing=4, font=LABEL):
    """Libellé en capitales espacées."""
    text = text.replace("&", "&amp;")
    return MarkupText(f'<span letter_spacing="{int(spacing * 180)}">{text}</span>', font=font, font_size=size,
                      color=color)


def neon(m, color, width=2.5, fill=None):
    """Néon affiné : trait fin, halo discret."""
    w = width * 0.6
    glow = VGroup(*[m.copy().set_fill(opacity=0).set_stroke(color, w * k, opacity=op)
                    for k, op in ((5, 0.03), (2.8, 0.07), (1.7, 0.16))])
    core = m.copy().set_stroke(color, w, opacity=1)
    if fill is not None:
        core.set_fill(fill, 1)
    return VGroup(glow, core)


def rail(points, color=DIMC, width=2):
    """Piste de circuit (polyligne à angles droits)."""
    return VMobject().set_points_as_corners([np.array(p, dtype=float) for p in points]).set_stroke(color, width * 0.65)


def flash_along(path, color, width=5, time_width=0.35, run_time=0.9):
    """Éclair lumineux qui parcourt une piste."""
    return ShowPassingFlash(path.copy().set_stroke(color, width * 0.65), time_width=time_width, run_time=run_time)


# --- Icônes ----------------------------------------------------------------------------------------
def icon_format(c):
    return Text("{ }", font=MONO, font_size=26, color=c)


def icon_scope(c):
    return VGroup(Circle(0.2), Circle(0.1), Dot(radius=0.035)).set_stroke(c, 2.5).set_fill(c, 0)\
        .add(Dot(radius=0.035, color=c))


def icon_lock(c):
    body = RoundedRectangle(corner_radius=0.04, width=0.34, height=0.26).set_stroke(c, 2.5)
    shackle = Arc(radius=0.11, start_angle=0, angle=PI).set_stroke(c, 2.5).next_to(body, UP, buff=0)
    return VGroup(body, shackle)


def icon_log(c):
    return VGroup(*[Line(LEFT * 0.18, RIGHT * (0.18 - 0.08 * (k % 2))).shift(DOWN * 0.11 * k)
                    for k in range(3)]).set_stroke(c, 2.5).center()


def icon_check(c, s=1.0):
    return VMobject().set_points_as_corners([[-0.2, 0, 0], [-0.06, -0.15, 0], [0.22, 0.17, 0]]).set_stroke(c, 5).scale(s)


def icon_cross(c, s=1.0):
    return VGroup(Line([-0.16, -0.16, 0], [0.16, 0.16, 0]), Line([-0.16, 0.16, 0], [0.16, -0.16, 0])).set_stroke(c, 5)\
        .scale(s)


def globe(r, c):
    g = VGroup(Circle(r), Ellipse(width=2 * r * 0.45, height=2 * r), Ellipse(width=2 * r, height=2 * r * 0.35),
               Line(UP * r, DOWN * r), Line(LEFT * r, RIGHT * r))
    return g.set_stroke(c, 2)


# --- La puce ----------------------------------------------------------------------------------------
class Chip(VGroup):
    def __init__(self, size=1.5, color=ICE, label_text="IA"):
        super().__init__()
        self.size, self.color = size, color
        body = RoundedRectangle(corner_radius=0.12, width=size, height=size)
        die = RoundedRectangle(corner_radius=0.06, width=size * 0.56, height=size * 0.56)
        pins = VGroup()
        for d in (UP, DOWN, LEFT, RIGHT):
            n = d[[1, 0, 2]] * np.array([1, 1, 0])  # direction le long du côté
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
