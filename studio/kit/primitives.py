"""Primitives: colours, fonts, neon, rails, flashes, icons — the minimal TRON vocabulary.

Every film builds from these. Colours carry meaning: cyan = meaning / MCP, orange = trust / harness,
ice = AI & text, red = error, green = validated, dim teal = unlit rails.
Fonts are macOS system fonts (DIN Alternate, Futura, Menlo).
"""

import numpy as np
from manim import *

config.background_color = "#000000"

# --- Colours -------------------------------------------------------------------------------------
CYAN = ManimColor("#00E5FF")      # MCP · meaning
ICE = ManimColor("#CFF8FF")       # AI, text
ORANGE = ManimColor("#FF9E1B")    # Harness · trust
RED = ManimColor("#FF3355")       # error, refusal
GREEN = ManimColor("#2BFF88")     # validated
DIMC = ManimColor("#1D3A44")      # unlit rails
BODY = ManimColor("#020A0F")      # block fill

# --- Fonts ----------------------------------------------------------------------------------------
LABEL = "DIN Alternate"
TITLE = "Futura"
MONO = "Menlo"


def label(text, size=20, color=ICE, spacing=4, font=LABEL):
    """Label in spaced capitals."""
    text = text.replace("&", "&amp;")
    return MarkupText(f'<span letter_spacing="{int(spacing * 180)}">{text}</span>', font=font, font_size=size,
                      color=color)


NEON_OPS = (0.03, 0.07, 0.16, 1.0)  # opacities of the 3 halo layers + core


def neon(m, color, width=2.5, fill=None):
    """Refined neon: thin stroke, discreet halo."""
    w = width * 0.6
    glow = VGroup(*[m.copy().set_fill(opacity=0).set_stroke(color, w * k, opacity=op)
                    for k, op in ((5, 0.03), (2.8, 0.07), (1.7, 0.16))])
    core = m.copy().set_stroke(color, w, opacity=1)
    if fill is not None:
        core.set_fill(fill, 1)
    return VGroup(glow, core)


def rail(points, color=DIMC, width=2):
    """Circuit rail (right-angle polyline)."""
    return VMobject().set_points_as_corners([np.array(p, dtype=float) for p in points]).set_stroke(color, width * 0.65)


def flash_along(path, color, width=5, time_width=0.35, run_time=0.9):
    """Flash of light running along a rail."""
    return ShowPassingFlash(path.copy().set_stroke(color, width * 0.65), time_width=time_width, run_time=run_time)


# --- Icons -----------------------------------------------------------------------------------------
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


def icon_user(c):
    head = Circle(0.15).set_stroke(c, 2.5)
    body = Arc(radius=0.28, start_angle=0, angle=PI).set_stroke(c, 2.5).next_to(head, DOWN, buff=0.06)
    return VGroup(head, body)


def icon_mail(c):
    env = Rectangle(width=0.5, height=0.34).set_stroke(c, 2)
    flap = VMobject().set_points_as_corners([env.get_corner(UL), env.get_center() + DOWN * 0.04, env.get_corner(UR)])
    return VGroup(env, flap.set_stroke(c, 2))


def icon_doc(c):
    page = Rectangle(width=0.34, height=0.44).set_stroke(c, 2)
    lines = VGroup(*[Line(LEFT * 0.1, RIGHT * 0.1).shift(UP * (0.1 - 0.1 * i)) for i in range(3)]).set_stroke(c, 1.6)
    return VGroup(page, lines.move_to(page))


def icon_sheet(c):
    grid = VGroup(Rectangle(width=0.46, height=0.36),
                  *[Line([-0.23, y, 0], [0.23, y, 0]) for y in (-0.06, 0.06)],
                  *[Line([x, -0.18, 0], [x, 0.18, 0]) for x in (-0.08, 0.08)])
    return grid.set_stroke(c, 1.8)


def icon_list(c):
    return VGroup(*[VGroup(Dot(radius=0.025), Line(ORIGIN, RIGHT * 0.22).shift(RIGHT * 0.06))
                    .shift(DOWN * 0.08 * i) for i in range(3)]).set_color(c).set_stroke(c, 1.6).center()


def icon_tool_card(color=CYAN):
    """Tool call as a visual: a mini card with a tool pictogram and two parameter pills."""
    box = RoundedRectangle(corner_radius=0.06, width=0.78, height=0.4)
    gear = VGroup(Circle(0.07), *[Line(UP * 0.09, UP * 0.13).rotate(a, about_point=ORIGIN) for a in np.arange(0, TAU, TAU / 6)])
    gear.set_stroke(color, 1.6).move_to(box.get_left() + RIGHT * 0.19)
    pills = VGroup(*[RoundedRectangle(corner_radius=0.04, width=0.17, height=0.09).set_fill(color, 0.9)
                     .set_stroke(width=0) for _ in range(2)]).arrange(DOWN, buff=0.05).move_to(box.get_center() + RIGHT * 0.15)
    card = VGroup(neon(box, color, 1.4, fill=BODY), gear, pills)
    return card.set_z_index(9)


def rack():
    """Server rack (unlit): body, slots, LEDs."""
    body = RoundedRectangle(corner_radius=0.04, width=0.42, height=1.12)
    slots = VGroup(*[Line([-0.14, 0.42 - 0.17 * i, 0], [0.07, 0.42 - 0.17 * i, 0]) for i in range(6)])
    leds = VGroup(*[Dot([0.13, 0.42 - 0.17 * i, 0], radius=0.024) for i in range(6)])
    return VGroup(neon(body, DIMC, 1.2, fill=BODY), slots.set_stroke(DIMC, 1.2),
                  leds.set_fill(DIMC, 1).set_stroke(width=0))


def square_dot(p, color=CYAN, s=0.075):
    """Small filled square (data point on a map)."""
    return Square(s).set_fill(color, 1).set_stroke(width=0).move_to(p)


def dimmed(mob, factor):
    """Static dim for states: every stroke / fill opacity × factor (neon halos stay proportional)."""
    for m in mob.family_members_with_points():
        m.set_stroke(opacity=m.get_stroke_opacity() * factor, family=False)
        m.set_fill(opacity=m.get_fill_opacity() * factor, family=False)
    return mob
