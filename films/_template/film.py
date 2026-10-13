"""<Film title> — engine film (Film / Act / Beat). Start from brief.md (G1), then write states only (G2).

    studio still <film>       # G2: one PNG per beat, no animation
    studio animatic <film>    # G3: default transitions (same id → morph, new → fade in, missing → fade out)
    studio dev <film>         # G4: custom motions where defined

Rules: a state is pure (build fresh mobjects every call); keywords only; dim until relevant; end on words.
"""

from manim import *

from studio.engine import Act, Beat, FilmScene
from studio.kit.actors import Chat, Chip, data_block
from studio.kit.layout import CHAT_C, CHAT_H, CHAT_W, CHIP_POS, DATA_Y
from studio.kit.primitives import CYAN, DIMC, ORANGE, label, rail

FR = {  # English on-screen text → French
    "AI": "IA", "DATA": "DONNÉES", "THE QUESTION": "LA QUESTION", "THE ANSWER": "LA RÉPONSE",
    "01 · THE QUESTION": "01 · LA QUESTION", "02 · THE ANSWER": "02 · LA RÉPONSE",
}


class Stage:
    """Factories shared by the states."""

    def __init__(self, tr):
        self.tr = tr

    def L(self, text, *a, **k):
        return label(self.tr(text), *a, **k)

    def chip(self):
        return Chip(label_text=self.tr("AI")).move_to(CHIP_POS)

    def chat(self, question):
        chat = Chat(CHAT_C, CHAT_W, CHAT_H, self.tr("CHAT · AI"))
        return chat, Chat.bubble(self.tr(question)).move_to(chat.bubble_pos(), aligned_edge=UR)


def s_question(st):
    chat, q = st.chat("THE QUESTION")
    chip = st.chip()
    return {"chat": chat, "q": q, "chip": chip, "in": rail([chat.win.get_right(), chip.port(LEFT)], DIMC, 2)}


def s_answer(st):
    cur = s_question(st)
    _, cur["data"] = data_block(10, [0, DATA_Y, 0], st.tr("DATA"))
    cur["reply"] = cur["chat"].reply("42", st.tr("THE ANSWER"), CYAN)
    return cur


def s_words(st):
    return {"word": st.L("THE ANSWER", 26, ORANGE, spacing=10)}


class Film(FilmScene):
    title = "Film title"
    FR = FR

    def build_stage(self):
        return Stage(self.tr)

    acts = [
        Act("question", "01 · THE QUESTION", "The question", [
            Beat("ask", s_question, note="The user asks; the AI listens."),
        ]),
        Act("answer", "02 · THE ANSWER", "The answer", [
            Beat("answer", s_answer, note="The data answers, in the chat."),
            Beat("words", s_words, morph_from={"word": "data"}, hold=2.0, note="End on words."),
        ]),
    ]
