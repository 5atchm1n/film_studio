"""AI strategy · assist ≠ automate — 30 s opener of the COMEX talk (Strategie_IA_COMEX_Indigo.pptx, slide 3).

Split screen, the AI chip in the middle: left = ASSIST (CRC agent's chat, customer history, a suggested reply the
agent validates), right = AUTOMATE (tickets → a rules / model ROUTER → agents; uncertain → a human). The chip is not
the router: automation is rules and decision models ("NOT AI" on the slide).

    studio still ai_strategy_comex --lang fr     # G2
"""

import numpy as np
from manim import *

from studio.engine import Act, Beat, FilmScene
from studio.kit.actors import Badge, Chat, Chip, Module, data_block, packet
from studio.kit.motions import send
from studio.kit.primitives import (BODY, CYAN, DIMC, GREEN, ICE, ORANGE, RED, dimmed, flash_along, icon_check, icon_user,
                                   label, neon, rail)

FR = {  # English on-screen text → French
    "AI": "IA", "STRATEGY": "STRATÉGIE", "BEYOND THE MYTH": "DÉPASSER LE MYTHE",
    "ASSIST · SLOW": "ASSISTER · LENT", "AUTOMATE · FAST": "AUTOMATISER · RAPIDE",
    "ASSIST": "ASSISTER", "AUTOMATE": "AUTOMATISER",
    "CHAT · AI": "CHAT · IA", "CRC · AGENT": "CRC · AGENT", "CUSTOMER REQUEST": "DEMANDE CLIENT",
    "CUSTOMER HISTORY": "HISTORIQUE CLIENT", "SUGGESTED REPLY": "RÉPONSE SUGGÉRÉE", "VALIDATED": "VALIDÉ",
    "HUMAN IN THE LOOP · ERROR CAUGHT": "HUMAIN DANS LA BOUCLE · ERREUR RATTRAPÉE",
    "TICKETS": "TICKETS", "ROUTER": "ROUTAGE", "RULES · MODELS": "RÈGLES · MODÈLES",
    "AGENT A": "AGENT A", "AGENT B": "AGENT B", "AGENT C": "AGENT C",
    "NO HUMAN · BOUNDED ERROR": "AUCUN HUMAIN · ERREUR BORNÉE", "UNCERTAIN": "INCERTAIN", "HUMAN": "HUMAIN",
    "01 · ONE WORD": "01 · UN MOT", "02 · ASSIST": "02 · ASSISTER", "03 · AUTOMATE": "03 · AUTOMATISER",
    "One word": "Un mot", "Assist": "Assister", "Automate": "Automatiser", "AI strategy": "Stratégie IA",
}

# --- Layout (split screen) ----------------------------------------------------------------------------------
ROW_Y = 0.35                                 # main row: chat · chip · tickets · router · agents
CHIP_C = np.array([0, ROW_Y, 0])
HEAD_Y, CAPTION_Y = 2.75, 2.3                # half titles, then their caption
LEFT_X, RIGHT_X = -3.6, 3.6                  # centres of the two halves
CHAT_C, CHAT_W, CHAT_H = np.array([-4.3, ROW_Y, 0]), 3.4, 2.2
HIST_C = np.array([-4.3, -2.55, 0])
INBOX_C = np.array([2.25, ROW_Y, 0])
ROUTER_C = np.array([4.2, ROW_Y, 0])
AGENT_X, AGENT_YS = 6.0, (ROW_Y + 1.1, ROW_Y, ROW_Y - 1.1)
HUMAN_C = np.array([4.2, -2.1, 0])
DIM = 0.3                                    # the other half, while one half is explained


class Stage:
    """Factories shared by the states (fresh mobjects on every call)."""

    def __init__(self, tr):
        self.tr = tr

    def L(self, text, *a, **k):
        return label(self.tr(text), *a, **k)

    # --- act 01 -----------------------------------------------------------------------------------------
    def title(self):
        ai, rest = self.L("AI", 40, ICE, spacing=14), self.L("STRATEGY", 40, ICE, spacing=14)
        row = VGroup(rest, ai) if self.tr("AI") != "AI" else VGroup(ai, rest)   # FR: STRATÉGIE IA
        row.arrange(RIGHT, buff=0.3).move_to([0, 0.5, 0])
        sub = self.L("BEYOND THE MYTH", 16, GREY_B, spacing=8).move_to([0, -0.45, 0])
        return {"title_ai": ai, "title_rest": rest, "subtitle": sub}

    def chip(self):
        c = Chip(label_text=self.tr("AI")).move_to(CHIP_C)
        return c

    def heads(self):
        return {"h_assist": self.L("ASSIST · SLOW", 16, CYAN, spacing=8).move_to([LEFT_X, HEAD_Y, 0]),
                "h_automate": self.L("AUTOMATE · FAST", 16, ORANGE, spacing=8).move_to([RIGHT_X, HEAD_Y, 0])}

    def job_rails(self, chip):
        return {"r_assist": rail([chip.port(LEFT), [CHAT_C[0] + CHAT_W / 2, ROW_Y, 0]], CYAN, 2),
                "r_automate": rail([chip.port(RIGHT), [INBOX_C[0] - 0.65, ROW_Y, 0]], ORANGE, 2)}

    # --- act 02 · assist ----------------------------------------------------------------------------------
    def assist(self, step):
        """step: 0 request · 1 suggested reply · 2 validated."""
        chip = self.chip()
        chat = Chat(CHAT_C, CHAT_W, CHAT_H, self.tr("CHAT · AI"))
        req = Chat.bubble(self.tr("CUSTOMER REQUEST")).move_to(chat.bubble_pos(), aligned_edge=UR)
        badge = Badge(self.tr("CRC · AGENT"), chat[0])
        _, hist = data_block(CHAT_W, HIST_C, self.tr("CUSTOMER HISTORY"))
        pin = chip.pin(1)
        hist_rail = rail([hist.get_right(), [pin[0], HIST_C[1], 0], pin], CYAN if step else DIMC, 2)
        out = {"chat": chat, "req": req, "badge": badge, "hist": hist, "hist_rail": hist_rail}
        if step >= 1:
            color = GREEN if step == 2 else CYAN
            box = RoundedRectangle(corner_radius=0.1, width=CHAT_W - 0.4, height=0.78).set_stroke(color, 1.4)
            box.set_fill(BODY, 1).move_to(chat.win.get_corner(DL) + np.array([0.2, 0.2, 0]), aligned_edge=DL)
            head = self.L("SUGGESTED REPLY", 9, color, spacing=3)
            lines = VGroup(*[Line(LEFT * w / 2, RIGHT * w / 2).set_stroke(color, 2, 0.85) for w in (1.9, 1.4)])
            body = VGroup(head, lines.arrange(DOWN, buff=0.13, aligned_edge=LEFT)).arrange(DOWN, buff=0.13,
                                                                                           aligned_edge=LEFT)
            body.move_to(box.get_left() + RIGHT * (0.2 + body.width / 2))
            reply = VGroup(box, body)
            if step == 2:
                ok = VGroup(icon_check(GREEN, 0.6), self.L("VALIDATED", 9, GREEN, spacing=3)).arrange(DOWN, buff=0.08)
                reply.add(ok.move_to(box.get_right() + LEFT * 0.55))
            out["reply"] = reply.set_z_index(4)   # after adding ✓: the whole reply draws above the chat
        if step == 2:
            out["cap_assist"] = self.L("HUMAN IN THE LOOP · ERROR CAUGHT", 11, GREY_B, spacing=3).move_to(
                [LEFT_X, CAPTION_Y, 0])
        return out

    # --- act 03 · automate --------------------------------------------------------------------------------
    def ticket(self, color=ORANGE, mark=None):
        box = RoundedRectangle(corner_radius=0.04, width=0.36, height=0.24).set_stroke(color, 1.4).set_fill(BODY, 1)
        if mark:
            return VGroup(box, Text(mark, font="Futura", font_size=16, color=color).move_to(box))
        lines = VGroup(*[Line(LEFT * w / 2, RIGHT * w / 2) for w in (0.2, 0.13)]).arrange(DOWN, buff=0.05,
                                                                                          aligned_edge=LEFT)
        return VGroup(box, lines.set_stroke(color, 1.4).move_to(box))

    def automate(self, step):
        """step: 0 tickets arrive · 1 routed · 2 one uncertain → human."""
        inbox = VGroup(*[self.ticket().shift(UP * 0.08 * k + RIGHT * 0.06 * k) for k in range(3)]).move_to(INBOX_C)
        inbox_lbl = self.L("TICKETS", 10, ORANGE, spacing=3).next_to(inbox, DOWN, 0.18)
        fork = VGroup(Line(LEFT * 0.16, ORIGIN), *[Line(ORIGIN, RIGHT * 0.16 + UP * 0.12 * k) for k in (-1, 0, 1)])
        router = Module(fork.set_stroke(ORANGE, 2.5), ROUTER_C, self.tr("ROUTER"), UP)
        rules = self.L("RULES · MODELS", 9, GREY_B, spacing=2).next_to(router, UP, 0.1)
        in_rail = rail([inbox.get_right() + RIGHT * 0.1, router[0].get_left()], ORANGE, 2)
        agents, a_rails = VGroup(), VGroup()
        for name, y in zip(("AGENT A", "AGENT B", "AGENT C"), AGENT_YS):
            lbl = self.L(name, 10, ORANGE, spacing=3)
            box = RoundedRectangle(corner_radius=0.06, width=1.3, height=0.42).move_to([AGENT_X, y, 0])
            agents.add(VGroup(neon(box, ORANGE, 1.2, fill=BODY), lbl.move_to(box)))
            mx = (ROUTER_C[0] + 0.3 + box.get_left()[0]) / 2
            a_rails.add(rail([router[0].get_right(), [mx, ROW_Y, 0], [mx, y, 0], box.get_left()],
                             ORANGE if step else DIMC, 2))
        out = {"inbox": inbox, "inbox_lbl": inbox_lbl, "in_rail": in_rail, "a_rails": a_rails, "router": router,
               "rules": rules, "agents": agents if step else dimmed(agents, 0.5)}
        if step >= 1:
            done = VGroup(*[self.ticket().scale(0.8).next_to(a, LEFT, 0.12) for a in agents])
            out["routed"] = done
            out["cap_automate"] = self.L("NO HUMAN · BOUNDED ERROR", 11, GREY_B, spacing=3).move_to(
                [RIGHT_X, CAPTION_Y, 0])
        if step == 2:
            person = icon_user(ICE).scale(0.8).move_to(HUMAN_C)
            out["human"] = VGroup(person, self.L("HUMAN", 10, ICE, spacing=3).next_to(person, DOWN, 0.12))
            out["h_rail"] = rail([router[0].get_bottom(), person.get_top() + UP * 0.12], RED, 2)
            q = self.ticket(RED, "?").next_to(person, RIGHT, 0.25)
            out["uncertain"] = VGroup(q, self.L("UNCERTAIN", 9, RED, spacing=2).next_to(q, RIGHT, 0.12))
        return out


def faded(pieces, f=DIM):
    return {k: dimmed(v, f) for k, v in pieces.items()}


# --- Act 01 · one word ----------------------------------------------------------------------------------------
def s_title(st):
    return st.title()


def s_two_jobs(st):
    chip = st.chip()
    return {**st.heads(), "chip": chip, **st.job_rails(chip)}


# --- Act 02 · assist --------------------------------------------------------------------------------------------
def assist_state(st, step):
    chip = st.chip()
    heads, rails = st.heads(), st.job_rails(chip)
    left = {"h_assist": heads["h_assist"], "r_assist": rails["r_assist"]}
    right = faded({"h_automate": heads["h_automate"], "r_automate": rails["r_automate"]})
    return {**left, **right, "chip": chip, **st.assist(step)}


def s_ask(st):
    return assist_state(st, 0)


def s_suggest(st):
    return assist_state(st, 1)


def s_validate(st):
    return assist_state(st, 2)


# --- Act 03 · automate ------------------------------------------------------------------------------------------
def automate_state(st, step, left_dim=DIM):
    chip = st.chip()
    heads, rails = st.heads(), st.job_rails(chip)
    left = faded({"h_assist": heads["h_assist"], "r_assist": rails["r_assist"], **st.assist(2)}, left_dim)
    return {**left, "chip": dimmed(chip, DIM), "r_automate": dimmed(rails["r_automate"], DIM),
            "h_automate": heads["h_automate"], **st.automate(step)}


def s_tickets(st):
    return automate_state(st, 0)


def s_route(st):
    return automate_state(st, 1)


def s_uncertain(st):
    return automate_state(st, 2)


# --- Motions (G4): deliberate on the assist side, rapid on the automate side ------------------------------------
def corners(r):
    """Corner points of a rail (right-angle polyline)."""
    return [*r.get_start_anchors(), r.get_end_anchors()[-1]]


def swap(sc, prev, cur, ids, run_time=0.4):
    """Morph the given ids from prev to cur (used at the start of a motion)."""
    sc.play(*[ReplacementTransform(prev[k], cur[k]) for k in ids], run_time=run_time)


def m_suggest(sc, prev, cur):
    """Slow: the history goes to the AI, which drafts a reply into the chat, line by line."""
    swap(sc, prev, cur, ["hist_rail"])
    p = packet(CYAN)
    send(sc, p, corners(cur["hist_rail"]), CYAN, run_time=1.0)
    sc.play(cur["chip"].pulse(CYAN), FadeOut(p), run_time=0.45)
    p = packet(CYAN)
    send(sc, p, corners(cur["r_assist"]), CYAN, run_time=1.0)
    box, (head, lines) = cur["reply"][0], cur["reply"][1]
    sc.play(FadeOut(p), Create(box), FadeIn(head), run_time=0.5)
    sc.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.6), run_time=0.7)


def m_route(sc, prev, cur):
    """Fast: a stream of tickets runs through the router and fans out to the agents, no human."""
    swap(sc, prev, cur, ["a_rails", "agents"])
    entry = corners(cur["in_rail"])
    paths = [rail(entry + corners(r)[1:]) for r in cur["a_rails"]]
    flying = [sc.stage.ticket().scale(0.6).move_to(entry[0]) for _ in range(9)]
    with sc.exact():
        sc.play(LaggedStart(*[MoveAlongPath(t, paths[k % 3], rate_func=rate_functions.ease_in_out_sine)
                              for k, t in enumerate(flying)], lag_ratio=0.22),
                flash_along(cur["router"][0][1], WHITE, 4, run_time=1.9), run_time=1.9)
    sc.play(*[FadeOut(t) for t in flying], FadeIn(cur["routed"]), FadeIn(cur["cap_automate"], shift=DOWN * 0.05),
            run_time=0.4)


def m_uncertain(sc, prev, cur):
    """One ticket the router cannot decide: it turns red and goes to a human."""
    entry = corners(cur["in_rail"])
    t = sc.stage.ticket().scale(0.6).move_to(entry[0])
    with sc.exact():
        sc.play(MoveAlongPath(t, rail(entry)), run_time=0.45, rate_func=rate_functions.ease_in_out_sine)
    q = cur["uncertain"][0].copy().move_to(cur["router"][0].get_center())
    sc.play(ReplacementTransform(t, q), Flash(cur["router"][0], color=RED, flash_radius=0.5, num_lines=10),
            run_time=0.4)
    sc.play(Create(cur["h_rail"]), FadeIn(cur["human"], shift=UP * 0.1), run_time=0.5)
    down = [cur["router"][0].get_bottom(), cur["h_rail"].get_end(), cur["uncertain"][0].get_center()]
    send(sc, q, down, RED, run_time=0.7)
    sc.play(FadeIn(cur["uncertain"][1], shift=LEFT * 0.05), run_time=0.3)
    sc.remove(q)


def s_words(st):
    a, neq, b = st.L("ASSIST", 30, CYAN, spacing=12), Text("≠", font="Futura", font_size=54, color=ICE), \
        st.L("AUTOMATE", 30, ORANGE, spacing=12)
    VGroup(a, neq, b).arrange(RIGHT, buff=0.6).move_to([0, 0.3, 0])
    return {"w_assist": a, "neq": neq, "w_automate": b}


class Film(FilmScene):
    title = "AI strategy"
    FR = FR

    def build_stage(self):
        return Stage(self.tr)

    acts = [
        Act("one_word", "01 · ONE WORD", "One word", [
            Beat("title", s_title, hold=2.2, note="Title card: STRATÉGIE IA · DÉPASSER LE MYTHE."),
            Beat("two_jobs", s_two_jobs, hold=2.0, morph_from={"chip": "title_ai"},
                 note="The title's AI becomes the chip; one rail to each side: ASSIST · SLOW / AUTOMATE · FAST."),
        ]),
        Act("assist", "02 · ASSIST", "Assist", [
            Beat("ask", s_ask, hold=1.2, note="Left half: the CRC agent's chat receives a customer request; "
                                                  "customer history below. Right half dimmed."),
            Beat("suggest", s_suggest, m_suggest, hold=0.8, note="History → AI → a SUGGESTED REPLY drafted in the chat."),
            Beat("validate", s_validate, hold=2.6, note="The agent validates (✓). HUMAN IN THE LOOP · ERROR CAUGHT."),
        ]),
        Act("automate", "03 · AUTOMATE", "Automate", [
            Beat("tickets", s_tickets, hold=1.6, note="Right half: tickets → ROUTER (rules · models, not the AI chip, "
                                                         "which dims). Left half dimmed."),
            Beat("route", s_route, m_route, hold=2.0, note="Routed straight to AGENT A / B / C. NO HUMAN · BOUNDED ERROR."),
            Beat("uncertain", s_uncertain, m_uncertain, hold=2.2, note="One uncertain ticket (?) goes to a human."),
            Beat("words", s_words, hold=3.0, morph_from={"w_assist": "h_assist", "w_automate": "h_automate"},
                 note="End on words: ASSIST ≠ AUTOMATE."),
        ]),
    ]
