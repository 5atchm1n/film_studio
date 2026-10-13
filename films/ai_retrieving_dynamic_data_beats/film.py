""""AI - Retrieving dynamic data", acts 01 and 06 re-expressed as beats (engine pilot).

Each beat is a pure state: {id: mobject}. Same ids morph between beats, new ids fade in, missing ids fade out.
Custom motions (full mode) reproduce the legacy gestures where they carry the concept.
Data, positions and the FR dictionary come from the legacy scene (../ai_retrieving_dynamic_data/legacy_scene.py).

    studio still ai_retrieving_dynamic_data_beats        # G2: one PNG per beat
    studio animatic ai_retrieving_dynamic_data_beats     # G3: default transitions only
    studio dev ai_retrieving_dynamic_data_beats          # full: custom motions where defined
"""

import sys
from pathlib import Path

import numpy as np
from manim import *

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ai_retrieving_dynamic_data"))
import legacy_scene as legacy  # noqa: E402  (data + FR only)

from studio.engine import Act, Beat, FilmScene, transition_anims  # noqa: E402
from studio.kit.actors import Badge, Chat, Chip, data_block, harness_clamps, harness_frame, packet  # noqa: E402
from studio.kit.layout import ANS_IN, BAND_Y, CHAT_C, CHAT_H, CHAT_W, CHIP_POS, DATA_Y, IN_X, OUT_Y  # noqa: E402
from studio.kit.motions import send  # noqa: E402
from studio.kit.primitives import (BODY, CYAN, DIMC, GREEN, ICE, LABEL, NEON_OPS, ORANGE, flash_along,  # noqa: E402
                                   globe, icon_check, icon_doc, icon_sheet, label, neon, rail)

FW = config.frame_width
PINS_ACT1 = [(s, k) for s in ("LEFT", "RIGHT") for k in (-1, 0, 1)]
PINS_ALL = PINS_ACT1 + [("UP", 0), ("DOWN", 0), ("DOWN", -1), ("DOWN", 1)]


class Stage:
    """Factories shared by the states (built fresh on every call: states stay pure)."""

    def __init__(self, tr):
        self.tr = tr

    def L(self, text, *a, **k):
        return label(self.tr(text), *a, **k)

    def chip(self, pins=(), scale=1.0):
        c = Chip(label_text=self.tr("AI")).move_to(CHIP_POS)
        c.hide_pins()
        for side, k in pins:
            for part, op in zip(c.pin_parts(side, k), NEON_OPS):
                part.set_stroke(opacity=op)
        if scale != 1.0:
            c.scale(scale)
            c.size *= scale
        return c

    # --- act 01 -------------------------------------------------------------------------------------
    def sources(self, frame_op=None):
        out = {}
        for k, name in enumerate(["WEB", "BOOKS", "WIKIS", "CODE", "ARTICLES", "FORUMS"]):
            col, row = divmod(k, 3)
            pos = np.array([-4.95 if col == 0 else 2.55, CHIP_POS[1] + 0.8 - 0.8 * row, 0])
            lbl = self.L(name, 12, CYAN, spacing=4)
            box = RoundedRectangle(corner_radius=0.06, width=lbl.width + 0.4, height=0.4).move_to(pos)
            frame = neon(box, CYAN, 1.2, fill=BODY)
            if frame_op is not None:
                frame.set_stroke(opacity=frame_op)
            out[f"src{k}"] = VGroup(frame, lbl.move_to(box))
        return out

    def traces(self, srcs, color=DIMC):
        chip, out = self.chip(), {}
        for k in range(6):
            col, row = divmod(k, 3)
            end = chip.port(LEFT if col == 0 else RIGHT) + UP * (1 - row) * 0.17 * chip.size
            edge = srcs[f"src{k}"][0][1]
            start = edge.get_right() if col == 0 else edge.get_left()
            mid_x = (start[0] + end[0]) / 2 + (row - 1) * 0.12 * (1 if col == 0 else -1)
            out[f"trace{k}"] = rail([start, [mid_x, start[1], 0], [mid_x, end[1], 0], end], color, 1.6)
        return out

    def public(self, op):
        return self.L("PUBLIC DATA", 13, CYAN, spacing=6).move_to(CHIP_POS + DOWN * 2.95).set_opacity(op)

    def use_cases(self, lit):
        tasks = [("WRITE A CLIENT EMAIL", "EMAIL READY"), ("SUMMARISE A CONTRACT", "5 KEY POINTS"),
                 ("WRITE AN EXCEL FORMULA", "FORMULA")]
        chip, out = self.chip(), {}
        for k, (task, result) in enumerate(tasks):
            y = CHIP_POS[1] + 0.8 - 0.8 * k
            off = (1 - k) * 0.17 * chip.size
            box = RoundedRectangle(corner_radius=0.06, width=3.25, height=0.46).move_to([-4.95, y, 0])
            icon = legacy.TASK_ICONS[k](ICE).scale_to_fit_height(0.24).move_to(box.get_left() + RIGHT * 0.3)
            out[f"in{k}"] = VGroup(neon(box, DIMC, 1.2, fill=BODY),
                                   self.L(task, 11, ICE, spacing=3).move_to(box.get_center() + RIGHT * 0.2), icon)
            res = VGroup(icon_check(GREEN, 0.55), self.L(result, 13, GREEN, spacing=3)).arrange(RIGHT, buff=0.15)
            res.move_to([2.3, y, 0], aligned_edge=LEFT).set_color(GREEN if lit else GREY_B)
            out[f"out{k}"] = res
            pl, pr = chip.port(LEFT) + UP * off, chip.port(RIGHT) + UP * off
            mx_l, mx_r = pl[0] - 0.35 - 0.12 * k, pr[0] + 0.35 + 0.12 * k
            c = GREEN if lit else DIMC
            out[f"left{k}"] = rail([[box.get_right()[0], y, 0], [mx_l, y, 0], [mx_l, pl[1], 0], pl], c, 1.6)
            out[f"right{k}"] = rail([pr, [mx_r, pr[1], 0], [mx_r, y, 0], [res.get_left()[0] - 0.12, y, 0]], c, 1.6)
        return out

    def chat(self, question):
        chat = Chat(CHAT_C, CHAT_W, CHAT_H, self.tr("CHAT · AI"))
        q = Chat.bubble(self.tr(question)).move_to(chat.bubble_pos(), aligned_edge=UR)
        return chat, q

    def io_rails(self):
        chip = self.chip()
        return {"in_rail": rail([[IN_X, OUT_Y, 0], chip.port(LEFT)], DIMC, 2),
                "out_rail": rail([chip.port(RIGHT), ANS_IN], DIMC, 2)}

    # --- act 06 -------------------------------------------------------------------------------------
    def together(self):
        """The condensed big picture at the start of act 06: chat · harness · MCP · data."""
        chat, q = self.chat(legacy.QUESTION_ME)
        reply = chat.reply(self.tr("0.31 M"), self.tr("OFF-STREET · WEST ZONE · 09/26"), GREEN)
        ok = icon_check(GREEN, 0.5).next_to(reply, RIGHT, 0.15).set_z_index(6)
        badge = Badge(" · ".join(self.tr(x) for x in legacy.USER_CTX[2]), chat[0])
        chip = self.chip(PINS_ALL, legacy.CHIP_IN_HARNESS)
        c, w, h = legacy.FRAME
        left, bottom = -3.02, c[1] - h / 2
        right = chip.get_right()[0] + 0.6 + 0.3 + 0.4          # the audit-log module + margin, as in the legacy condense
        top = chip.get_top()[1] + 0.65
        box = RoundedRectangle(corner_radius=0.18, width=right - left, height=top - bottom)
        box.move_to([(left + right) / 2, (top + bottom) / 2, 0])
        h_lbl = self.L("HARNESS", 20, ORANGE, spacing=10).scale(0.75).move_to([box.get_x(), box.get_top()[1] - 0.28, 0])
        harness = VGroup(harness_frame(box), h_lbl, harness_clamps(box, OUT_Y, CHIP_POS[0]))
        mid = (left + right) / 2
        band_box = RoundedRectangle(corner_radius=0.12, width=right - left, height=0.9).move_to([mid, BAND_Y, 0])
        mcp_lbl = VGroup(self.L("MCP", 20, CYAN, spacing=6), self.L("MODEL CONTEXT PROTOCOL", 8, CYAN, spacing=1))
        mcp_lbl.arrange(DOWN, buff=0.06).move_to(band_box)
        mcp = VGroup(neon(band_box, CYAN, 2, fill=ManimColor("#021B21")), mcp_lbl)
        _, data = data_block(right - left, [mid, DATA_Y, 0], self.tr("DATA"))
        top_pin = chip.port(DOWN)
        trunk = rail([top_pin, [top_pin[0], band_box.get_top()[1], 0]], CYAN, 2).set_stroke(opacity=0.5)
        link = rail([band_box.get_bottom(), data.get_top() + UP * 0.05], CYAN, 1.6).set_stroke(opacity=0.5)
        return {"chat": chat, "q": q, "reply": reply, "ok": ok, "badge": badge, **self.io_rails(),
                "harness": harness, "chip": chip, "trunk": trunk, "mcp": mcp, "link": link, "data": data}

    def deliverables(self, box):
        bars = VGroup(*[Rectangle(width=0.1, height=h).set_fill(GREEN, 0.8).set_stroke(width=0)
                        for h in (0.18, 0.32, 0.24, 0.42)]).arrange(RIGHT, buff=0.05, aligned_edge=DOWN)
        outs = VGroup()
        for icon, name in [(icon_sheet(GREEN), "TABLES"), (bars, "CHARTS"), (icon_doc(GREEN), "REPORTS")]:
            outs.add(VGroup(icon, self.L(name, 9, GREEN, spacing=3)).arrange(DOWN, buff=0.15))
        return outs.arrange(RIGHT, buff=0.5).move_to([(box.get_right()[0] + FW / 2) / 2 + 0.2, OUT_Y + 0.3, 0])

    def words(self):
        w1 = self.L("TRUST", 26, ORANGE, spacing=10)
        w2 = self.L("SEMANTIC LAYER", 26, CYAN, spacing=10)
        w3 = self.L("RETRIEVING DYNAMIC DATA", 20, WHITE, spacing=8)
        VGroup(w1, w2, w3).arrange(DOWN, buff=0.55).move_to([0, 0.2, 0])
        return w1, w2, w3


# --- Act 01 · The AI ---------------------------------------------------------------------------------------
def s_sources(st):
    return {**st.sources(), "public": st.public(0.3)}


def s_chip_born(st):
    srcs = st.sources(frame_op=0.6)
    return {**srcs, **st.traces(srcs), "chip": st.chip(PINS_ACT1), "public": st.public(1)}


def m_chip_born(sc, prev, cur):
    """Circuit weaving: rails grow from the sources, energy draws the chip, the words melt into it."""
    chip = cur["chip"]
    traces = [cur[f"trace{k}"].copy().set_stroke(CYAN) for k in range(6)]
    sc.play(LaggedStart(*[Create(t) for t in traces], lag_ratio=0.03),
            *[prev[f"src{k}"][0].animate.set_stroke(opacity=0.25) for k in range(6)], run_time=1.0)
    sc.play(*[flash_along(t, WHITE, 4, run_time=1.0) for t in traces], Create(chip.body), Create(chip.wires),
            prev["public"].animate.set_opacity(1), run_time=0.8)
    sc.play(Create(chip.die), Create(chip.pins, lag_ratio=0.05), run_time=0.6)
    ghosts = [prev[f"src{k}"][1].copy() for k in range(6)]
    sc.play(*[g.animate(rate_func=rate_functions.ease_in_cubic).move_to(chip.get_center()).scale(0.3).set_opacity(0)
              for g in ghosts], FadeIn(chip.label), *[ReplacementTransform(t, cur[f"trace{k}"]) for k, t in enumerate(traces)],
            *[ReplacementTransform(prev[f"src{k}"], cur[f"src{k}"]) for k in range(6)], chip.pulse(CYAN), run_time=0.7)
    sc.remove(*ghosts)


def s_use_cases(st):
    return {**st.use_cases(lit=False), "chip": st.chip(PINS_ACT1), "public": st.public(0.3)}


USE_CASE_PAIRS = {**{f"in{k}": f"src{k}" for k in range(3)}, **{f"out{k}": f"src{3 + k}" for k in range(3)},
                  **{f"left{k}": f"trace{k}" for k in range(3)}, **{f"right{k}": f"trace{3 + k}" for k in range(3)}}


def s_general_ai(st):
    cur = {**st.use_cases(lit=True), "chip": st.chip(PINS_ACT1), "public": st.public(0.3)}
    tag = VGroup(st.L("GENERAL AI", 18, ICE, spacing=8), st.L("FAST · VERSATILE", 11, GREY_B, spacing=4))
    cur["tag"] = tag.arrange(DOWN, buff=0.1).next_to(cur["chip"], UP, 0.35)
    return cur


def m_general_ai(sc, prev, cur):
    """Each example runs through the circuit very fast: rail and result turn green."""
    with sc.exact():
        for k in range(3):
            sc.play(*[ReplacementTransform(prev[f"{p}{k}"], cur[f"{p}{k}"]) for p in ("left", "right", "out")],
                    prev["chip"].pulse(GREEN), run_time=0.35)
    sc.play(FadeIn(cur["tag"], shift=UP * 0.1), run_time=0.35)


def s_question(st):
    chat, q = st.chat("OUR CAR PARKS · PARIS?")
    return {"chat": chat, "q": q, **st.io_rails(), "chip": st.chip(PINS_ACT1), "public": st.public(0.3)}


def s_web_guess(st):
    cur = s_question(st)
    cur["chip"] = st.chip(PINS_ACT1 + [("UP", 0)])
    web = neon(globe(0.42, CYAN).move_to([2.2, 3.05, 0]), CYAN, 1.6)
    top = cur["chip"].port(UP)
    cur.update(web=web, web_lbl=st.L("INTERNET", 11, CYAN, spacing=4).next_to(web, RIGHT, 0.2),
               web_rail=rail([top, [top[0], 3.05, 0], web.get_left()], CYAN, 1.6),
               mem=st.L("MEMORY", 11, CYAN, spacing=4).next_to(cur["chip"], DOWN, 0.3))
    win = cur["chat"].win
    a_box = RoundedRectangle(corner_radius=0.1, width=CHAT_W - 0.4, height=0.72).set_stroke(ORANGE, 1.4)
    a_box.set_fill(BODY, 1).move_to(win.get_corner(DL) + np.array([0.2, 0.2, 0]), aligned_edge=DL).set_z_index(4)
    final = VGroup(Text("?", font=LABEL, font_size=32, color=ORANGE), st.L("SOURCE: WEB", 10, ORANGE, spacing=2))
    cur["answer"] = VGroup(a_box, final.arrange(RIGHT, buff=0.3).move_to(a_box).set_z_index(5))
    return cur


def m_web_guess(sc, prev, cur):
    """The question goes to the chip, which looks it up on the web and guesses."""
    chip = prev["chip"]
    p = packet(ICE)
    send(sc, p, [[IN_X, OUT_Y, 0], chip.port(LEFT)], ICE, run_time=0.4)
    sc.play(chip.pulse(), FadeOut(p), run_time=0.35)
    sc.play(Create(cur["web_rail"]), FadeIn(cur["web"]), FadeIn(cur["web_lbl"]), FadeIn(cur["mem"]),
            ReplacementTransform(chip, cur["chip"]), run_time=0.5)
    pts = [cur["chip"].port(UP), [cur["chip"].port(UP)[0], 3.05, 0], cur["web"].get_left()]
    p = packet(CYAN)
    send(sc, p, pts + list(reversed(pts))[1:], CYAN, run_time=0.55)
    sc.remove(p)
    p = packet(ORANGE)
    send(sc, p, [cur["chip"].port(LEFT), [IN_X, OUT_Y, 0]], ORANGE, run_time=0.3)
    sc.play(FadeOut(p), Create(cur["answer"][0]), FadeIn(cur["answer"][1], scale=1.3), run_time=0.55)


# --- Act 06 · Together -------------------------------------------------------------------------------------
def s_circuit(st):
    return st.together()


def m_circuit(sc, prev, cur):
    """Arriving from the previous state, then the whole circuit lights up once; harness and band flash."""
    anims, swaps = transition_anims(prev, cur)
    for old, new in swaps:
        sc.remove(old)
        sc.add(new)
    sc.play(*anims, run_time=0.8, rate_func=rate_functions.ease_in_out_cubic)
    sc.play(flash_along(cur["in_rail"], WHITE, 5, run_time=0.9), flash_along(cur["trunk"], WHITE, 5, run_time=0.9),
            flash_along(cur["link"], WHITE, 5, run_time=0.9), cur["chip"].pulse(), run_time=0.9)
    sc.play(flash_along(cur["harness"][0][1], ORANGE, 6, time_width=0.4, run_time=0.8),
            flash_along(cur["mcp"][0][1], CYAN, 6, time_width=0.4, run_time=0.8), run_time=0.8)


def s_deliverables(st):
    cur = st.together()
    cur["reply"].shift(UP * 0.04)
    cur["ok"].shift(UP * 0.04)
    cur["outs"] = st.deliverables(cur["harness"][0][1])
    return cur


def m_deliverables(sc, prev, cur):
    """The answer turns into tables, charts, reports."""
    sc.play(ReplacementTransform(prev["reply"], cur["reply"]), ReplacementTransform(prev["ok"], cur["ok"]), run_time=0.2)
    src = cur["reply"].copy()
    sc.play(src.animate.move_to(cur["outs"]).scale(0.8), run_time=0.7)
    sc.play(FadeOut(src, scale=0.6), LaggedStart(*[FadeIn(o, scale=0.8) for o in cur["outs"]], lag_ratio=0.2),
            run_time=0.9)


def s_to_chat(st):
    cur = s_deliverables(st)
    back = VGroup(*[o[0].copy() for o in cur["outs"]]).scale(0.45).arrange(RIGHT, buff=0.22)
    cur["back"] = back.next_to(cur["reply"], DOWN, 0.06).align_to(cur["reply"], LEFT).set_z_index(6)
    return cur


def m_to_chat(sc, prev, cur):
    """Sent back to the user in all these forms: they arrive in the chat."""
    back = VGroup(*[o[0].copy() for o in prev["outs"]]).set_z_index(6)
    sc.play(LaggedStart(*[b.animate(path_arc=PI / 5).move_to(d).scale(0.45) for b, d in zip(back, cur["back"])],
                        lag_ratio=0.15), flash_along(prev["in_rail"], GREEN, 5, run_time=1.0), run_time=1.1)
    sc.play(Flash(prev["chat"][0], color=GREEN, flash_radius=1.9, num_lines=14), run_time=0.7)
    sc.remove(back)


def s_blocks(st):
    t = st.together()
    blocks = VGroup(t["harness"], t["mcp"], t["data"]).scale(0.8).move_to([0, 0.2, 0])
    return {"harness": blocks[0], "mcp": blocks[1], "data": blocks[2]}


def s_words(st):
    w1, w2, _ = st.words()
    return {"trust": w1, "semantic": w2}


def s_understanding(st):
    w1, w2, _ = st.words()
    return {"trust": w1, "understanding": st.L("UNDERSTANDING", 26, CYAN, spacing=10).move_to(w2)}


def s_retrieving(st):
    w1, w2, w3 = st.words()
    return {**s_understanding(st), "retrieving": w3}


class Film(FilmScene):
    title = "AI - Retrieving dynamic data"
    FR = legacy.FR

    def build_stage(self):
        return Stage(self.tr)

    acts = [
        Act("ai", "01 · THE AI", "General AI", [
            Beat("sources", s_sources, hold=0.4, note="Six public sources; PUBLIC DATA dimmed until relevant."),
            Beat("chip_born", s_chip_born, m_chip_born, hold=0.3,
                 note="Right-angle rails from every source; the chip is born from the data."),
            Beat("use_cases", s_use_cases, hold=0.3, morph_from=USE_CASE_PAIRS,
                 note="Sources morph into tasks (left) and results (right)."),
            Beat("general_ai", s_general_ai, m_general_ai, hold=0.9,
                 note="Each example runs through the circuit: results turn green. GENERAL AI · FAST · VERSATILE."),
            Beat("question", s_question, hold=0.4, note="A question about OUR business, typed in the chat."),
            Beat("web_guess", s_web_guess, m_web_guess, hold=0.5,
                 note="The AI looks it up on the web and guesses: ? · SOURCE: WEB."),
        ]),
        Act("together", "06 · TOGETHER", "Together", [
            Beat("circuit", s_circuit, m_circuit, hold=0.4,
                 note="Big picture: chat → harness → MCP → data; the whole circuit lights up once."),
            Beat("deliverables", s_deliverables, m_deliverables, hold=0.3,
                 note="The answer becomes tables, charts, reports."),
            Beat("to_chat", s_to_chat, m_to_chat, hold=1.0, note="…sent back to the user, in the chat."),
            Beat("blocks", s_blocks, hold=0.3, run_time=0.9, note="Only the three blocks remain, re-centred."),
            Beat("words", s_words, hold=1.0, run_time=1.2, morph_from={"trust": "harness", "semantic": "mcp"},
                 note="Harness → TRUST, MCP → SEMANTIC LAYER; data fades."),
            Beat("understanding", s_understanding, hold=0.6, run_time=0.9, morph_from={"understanding": "semantic"},
                 note="SEMANTIC LAYER → UNDERSTANDING."),
            Beat("retrieving", s_retrieving, hold=3.0, run_time=0.9, note="End on words: RETRIEVING DYNAMIC DATA."),
        ]),
    ]
