"""Kit gallery: one still per primitive, actor and motion (motions: start · middle · end).

    studio gallery        # renders gallery/*.png, gallery/sheet.png and gallery/README.md

Each piece is a small function below: add one when the kit grows.
"""

import json
import os
from pathlib import Path

import numpy as np
from manim import *
from PIL import Image

from studio.kit.actors import (Badge, Band, Chat, Chip, CodeFile, Module, data_block, harness_clamps, harness_frame,
                               packet, panel_frame)
from studio.kit.layout import CHAT_C, CHAT_H, CHAT_W, CHIP_POS, OUT_Y
from studio.kit.motions import condense_anims, dim, highlight, morph_anims, words_anims
from studio.kit.primitives import (BODY, CYAN, DIMC, GREEN, ICE, MONO, ORANGE, RED, TITLE, flash_along, globe,
                                   icon_check, icon_cross, icon_doc, icon_format, icon_list, icon_lock, icon_log,
                                   icon_mail, icon_scope, icon_sheet, icon_tool_card, icon_user, label, neon, rack, rail,
                                   square_dot)
from studio.kit.scene import StudioScene

OUT = Path(os.environ.get("GALLERY_OUT", "gallery"))


def caption(text):
    return label(text, 11, GREY_B, spacing=4).to_corner(DL, buff=0.3)


def settle(anims, alpha):
    """Show animations frozen at `alpha` (0 = start, 1 = end). Returns the mobjects to add."""
    g = AnimationGroup(*anims)
    g.begin()
    g.interpolate(alpha)
    return g.mobject


# --- Primitives --------------------------------------------------------------------------------------
def p_palette():
    rows = VGroup()
    for k, (name, c, meaning) in enumerate([("CYAN", CYAN, "MEANING · MCP"), ("ORANGE", ORANGE, "TRUST · HARNESS"),
                                            ("ICE", ICE, "AI · TEXT"), ("RED", RED, "ERROR"),
                                            ("GREEN", GREEN, "VALIDATED"), ("DIMC", DIMC, "UNLIT RAIL")]):
        y = 1.6 - 0.65 * k
        sw = RoundedRectangle(corner_radius=0.06, width=0.9, height=0.45).set_fill(c, 1).set_stroke(width=0)
        rows.add(sw.move_to([-2.2, y, 0]),
                 label(name, 12, c if c is not DIMC else GREY_B, spacing=4).move_to([-1.4, y, 0], aligned_edge=LEFT),
                 label(meaning, 11, GREY_B, spacing=3).move_to([0.6, y, 0], aligned_edge=LEFT))
    return [rows.move_to(ORIGIN)]


def p_type():
    g = VGroup(label("DIN ALTERNATE · SPACED CAPS", 22, ICE, spacing=6),
               Text("1.12 M", font=TITLE, font_size=44, color=CYAN),
               Text("data = mcp.call(tool, scope)", font=MONO, font_size=22, color=ORANGE),
               label("KEYWORDS · NEVER SENTENCES", 12, GREY_B, spacing=4))
    return [g.arrange(DOWN, buff=0.45)]


def p_neon():
    boxes = VGroup(*[neon(RoundedRectangle(corner_radius=0.12, width=2.6, height=1.5), c, w, fill=BODY)
                     for c, w in ((CYAN, 2), (ORANGE, 2), (ICE, 1.6))]).arrange(RIGHT, buff=0.6)
    return [boxes]


def p_rails():
    pts = [[-5, 1.2, 0], [-2, 1.2, 0], [-2, -0.8, 0], [3, -0.8, 0], [3, 0.6, 0], [5, 0.6, 0]]
    base = rail(pts, DIMC, 2)
    lit = rail([[-5, -2, 0], [0, -2, 0], [0, -1.4, 0], [5, -1.4, 0]], CYAN, 2)
    flash = settle([flash_along(lit, WHITE, 5)], 0.5)
    return [base, lit, flash, label("RIGHT ANGLES ONLY · FLASH ALONG", 10, GREY_B, spacing=3).move_to([0, 2.3, 0])]


def p_icons():
    items = [("FORMAT", icon_format(ORANGE)), ("SCOPE", icon_scope(ORANGE)), ("LOCK", icon_lock(ORANGE)),
             ("LOG", icon_log(ORANGE)), ("CHECK", icon_check(GREEN)), ("CROSS", icon_cross(RED)),
             ("USER", icon_user(ICE)), ("MAIL", icon_mail(ICE)), ("DOC", icon_doc(ICE)), ("SHEET", icon_sheet(ICE)),
             ("LIST", icon_list(ORANGE)), ("TOOL CARD", icon_tool_card(CYAN)), ("GLOBE", globe(0.35, CYAN)),
             ("RACK", rack().scale(0.6)), ("DOT", square_dot(ORIGIN, CYAN, 0.12))]
    cells = VGroup(*[VGroup(m.scale_to_fit_height(min(0.6, m.height)), label(n, 9, GREY_B, spacing=2))
                     .arrange(DOWN, buff=0.2) for n, m in items])
    return [cells.arrange_in_grid(3, 5, buff=(0.9, 0.6))]


# --- Actors ------------------------------------------------------------------------------------------
def a_chip():
    full = Chip(label_text="AI").move_to(LEFT * 2.5)
    bare = Chip(label_text="AI").move_to(RIGHT * 2.5)
    bare.hide_pins()
    for side, k in (("LEFT", 0), ("DOWN", 0)):
        for part in bare.pin_parts(side, k):
            part.set_stroke(opacity=1)
    return [full, bare, label("ALL PINS", 10, GREY_B, spacing=3).next_to(full, DOWN, 0.5),
            label("PINS SHOWN WHEN CONNECTED", 10, GREY_B, spacing=3).next_to(bare, DOWN, 0.5)]


def a_chat():
    chat = Chat(CHAT_C + RIGHT * 3.2, CHAT_W, CHAT_H)
    q = Chat.bubble("PARKING SESSIONS · SEPT.?").move_to(chat.bubble_pos(), aligned_edge=UR)
    ans = chat.reply("0.31 M", "OFF-STREET · WEST ZONE · 09/26", GREEN)
    badge = Badge("INDIGO · DIRECTOR · WEST ZONE", chat[0])
    return [chat, q, ans, badge]


def a_panel():
    box, frame, title = panel_frame(-1.35, 0, "TOOL CALL", icon_tool_card(CYAN).scale(0.55).set_z_index(0), CYAN)
    pills = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.05, width=1.2, height=0.28).set_stroke(CYAN, 1.1, 0.8)
                            .set_fill(BODY, 1), label(t, 7, CYAN, spacing=1))
                     for t in ("ON-STREET", "OFF-STREET", "CAR PARKS", "ZONES")])
    for p in pills:
        p[1].move_to(p[0])
    pills.arrange_in_grid(2, 2, buff=(0.1, 0.08)).move_to(box)
    return [frame, title, pills]


def a_band():
    band = Band(12, 1.0, [0, 0.6, 0], "MCP", "MODEL CONTEXT PROTOCOL")
    band.label.move_to([-5.0, 0.6, 0])
    _, data = data_block(12, [0, -1.2, 0], "DATA")
    return [band.frame(), band.label, data, label("BAND · DATA BLOCK", 10, GREY_B, spacing=3).move_to([0, 2.2, 0])]


def a_harness():
    chip = Chip(label_text="AI").scale(0.8).move_to(CHIP_POS)
    chip.size *= 0.8
    box = RoundedRectangle(corner_radius=0.18, width=6.0, height=3.4).move_to(CHIP_POS + DOWN * 0.55 + RIGHT * 0.8)
    mods = VGroup(Module(icon_format(ORANGE), [-2.55, OUT_Y, 0], "FORMAT", DOWN),
                  Module(icon_scope(ORANGE), [-1.2, -0.25, 0], "SCOPE", LEFT),
                  Module(icon_lock(ORANGE), [-1.2, -0.9, 0], "RIGHTS", LEFT),
                  Module(icon_log(ORANGE), [1.0, OUT_Y, 0], "TRACE", DOWN))
    return [harness_frame(box), harness_clamps(box, OUT_Y, CHIP_POS[0]), chip, mods,
            label("HARNESS", 20, ORANGE, spacing=10).next_to(box, UP, 0.3)]


def a_codefile():
    code = CodeFile(-3.0, 3.0, 0, ["check_format(question)", "tools = mcp.list_tools()", "scope = user.zone()",
                                   "assert user.can_read(tool)", "data = mcp.call(tool, scope)"])
    code[1].clear_updaters()
    code.lines[1].set_color(GREEN)
    code.lines[2].set_color(ORANGE)
    code.cursor.set_opacity(1).next_to(code.lines[2], LEFT, 0.1)
    return [code]


def a_packet():
    pts = [[-5, 0.5, 0], [-1, 0.5, 0], [-1, -0.8, 0], [5, -0.8, 0]]
    r = rail(pts, DIMC, 2)
    trail = rail([[-2.4, 0.5, 0], [-1, 0.5, 0], [-1, -0.3, 0]], CYAN, 3)
    p = packet(CYAN).move_to([-1, -0.3, 0])
    return [r, trail, p]


# --- Motions (start · middle · end) -------------------------------------------------------------------
def m_morph(alpha):
    blocks = VGroup(*[neon(RoundedRectangle(corner_radius=0.1, width=2.2, height=1.0), c, 2, fill=BODY)
                      for c in (ORANGE, CYAN, CYAN)]).arrange(RIGHT, buff=0.5)
    words = VGroup(label("TRUST", 26, ORANGE, spacing=10), label("MEANING", 26, CYAN, spacing=10)).arrange(DOWN, buff=0.5)
    return [settle(morph_anims(blocks, words), alpha)]


def m_send(alpha):
    pts = [[-5, 1, 0], [0, 1, 0], [0, -1, 0], [5, -1, 0]]
    r = rail(pts, DIMC, 2)
    p = packet(ICE).move_to(r.point_from_proportion(alpha))
    return [r, p, Dot(pts[0], color=ICE), Dot(pts[-1], color=CYAN)]


def m_dim(alpha):
    g = VGroup(neon(RoundedRectangle(corner_radius=0.1, width=3, height=1.2), CYAN, 2, fill=BODY),
               label("NOT RELEVANT YET", 12, CYAN, spacing=4))
    hot = VGroup(neon(RoundedRectangle(corner_radius=0.1, width=3, height=1.2), ORANGE, 2, fill=BODY),
                 label("IN USE", 12, ORANGE, spacing=4)).shift(RIGHT * 3.5)
    g.shift(LEFT * 3.5)
    settle([dim([g], 0.25)], alpha)  # dim works in place on g
    return [g, hot]


def m_highlight(alpha):
    r = rail([[-5, 0, 0], [-1, 0, 0], [-1, -1, 0], [5, -1, 0]], DIMC, 2)
    on, _restore = highlight(r, CYAN, 3)
    return [settle([on], alpha), label("IN PLACE · NO LIT COPY", 10, GREY_B, spacing=3).move_to([0, 1.5, 0])]


def m_rise(alpha):
    src = label("WHAT DOES OUR DATA MEAN?", 14, ICE, spacing=4).move_to(ORIGIN)
    ttl = label("04 · WHAT DOES OUR DATA MEAN?", 14, GREY_B, spacing=6)
    ttl.move_to(np.array([-config.frame_width / 2 + 0.45, config.frame_height / 2 - 0.4, 0]), aligned_edge=UL)
    return [settle([FadeTransform(src, ttl)], alpha)]


def m_condense(alpha):
    pills = VGroup(*[neon(RoundedRectangle(corner_radius=0.06, width=1.6, height=0.4), CYAN, 1.4, fill=BODY)
                     for _ in range(5)]).arrange(RIGHT, buff=0.25).move_to([0, 1, 0])
    tables = VGroup(*[RoundedRectangle(corner_radius=0.05, width=1.0, height=0.36).set_stroke(DIMC, 1.5)
                      for _ in range(8)]).arrange(RIGHT, buff=0.2).move_to([0, -1.2, 0])
    icon = Module(icon_list(CYAN), [0, 1, 0], color=CYAN)
    _, data = data_block(10, [0, -1.2, 0], "DATA")
    return [settle(condense_anims([(pills, icon), (tables, data)]), alpha)]


def m_words(alpha):
    h = neon(RoundedRectangle(corner_radius=0.18, width=4, height=1.6), ORANGE, 2).move_to([0, 1, 0])
    m = neon(RoundedRectangle(corner_radius=0.12, width=5, height=0.8), CYAN, 2).move_to([0, -0.6, 0])
    d = neon(RoundedRectangle(corner_radius=0.12, width=5, height=0.6), CYAN, 1.6).move_to([0, -1.7, 0])
    w1, w2 = label("TRUST", 26, ORANGE, spacing=10).move_to([0, 1, 0]), label("UNDERSTANDING", 26, CYAN, spacing=10)
    w2.move_to([0, -0.6, 0])
    return [settle(words_anims([(h, w1), (m, w2)], fade=[d]), alpha)]


PIECES = [  # (file name, caption, description, builder, is_motion)
    ("p01_palette", "PALETTE", "Colours carry meaning", p_palette, False),
    ("p02_type", "TYPE", "DIN Alternate labels, Futura numbers, Menlo code", p_type, False),
    ("p03_neon", "NEON", "neon(): thin stroke + discreet halo", p_neon, False),
    ("p04_rails", "RAILS", "rail() right angles; flash_along()", p_rails, False),
    ("p05_icons", "ICONS", "icon_* pictograms, globe, rack, square_dot", p_icons, False),
    ("a01_chip", "CHIP", "Chip: the AI; pins appear when connected", a_chip, False),
    ("a02_chat", "CHAT", "Chat (question bubble, reply) + Badge (user identity)", a_chat, False),
    ("a03_panel", "PANEL", "panel_frame(): the side that explains the mechanism", a_panel, False),
    ("a04_band", "BAND · DATA", "Band (semantic layer / MCP) and data_block()", a_band, False),
    ("a05_harness", "HARNESS", "harness_frame(), harness_clamps(), Module", a_harness, False),
    ("a06_codefile", "CODE FILE", "CodeFile: lines light up as they run (step / reset)", a_codefile, False),
    ("a07_packet", "PACKET", "packet() travelling on a rail (motions.send)", a_packet, False),
    ("m01_morph", "MORPH", "morph(): elements pair up and transform", m_morph, True),
    ("m02_send", "SEND", "send(): a packet travels along a rail", m_send, True),
    ("m03_dim", "DIM / LIGHT", "dim() until relevant, light() when used", m_dim, True),
    ("m04_highlight", "HIGHLIGHT", "highlight(): recolour in place, returns a restore", m_highlight, True),
    ("m05_rise", "RISE TO TITLE", "rise_to_title(): a finding becomes the chapter label", m_rise, True),
    ("m06_condense", "CONDENSE", "condense(): details → big-picture blocks", m_condense, True),
    ("m07_words", "WORDS FROM BLOCKS", "words_from_blocks(): end on words", m_words, True),
]


class Gallery(StudioScene):
    def snap(self, mobs, text):
        self.clear()
        self.add(*mobs, caption(text))
        self.renderer.update_frame(self, ignore_skipping=True)
        return Image.fromarray(self.renderer.get_frame()).convert("RGB")

    def construct(self):
        OUT.mkdir(parents=True, exist_ok=True)
        index = []
        for name, cap, desc, build, motion in PIECES:
            if motion:  # 2 × 2: start · middle / end · what it does
                shots = [self.snap(build(a), f"{cap} · {t}") for a, t in ((0, "START"), (0.5, "MIDDLE"), (1, "END"))]
                shots.append(self.snap([label(cap, 30, ICE, spacing=8).move_to(UP * 0.4),
                                        Text(desc, font=MONO, font_size=20, color=GREY_B).move_to(DOWN * 0.5)], ""))
                w, h = shots[0].size
                img = Image.new("RGB", (w + 4, h + 4), "#0b0f12")
                for k, sh in enumerate(shots):
                    img.paste(sh.resize((w // 2, h // 2), Image.LANCZOS), ((k % 2) * (w // 2 + 4), (k // 2) * (h // 2 + 4)))
            else:
                img = self.snap(build(), cap)
            img.save(OUT / f"{name}.png")
            index.append([name, cap, desc])
        (OUT / "index.json").write_text(json.dumps(index, indent=1))
