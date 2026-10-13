"""Film / Act / Beat: one film description, three render modes (FILM_MODE).

A beat is a *state* of the screen: `state(stage)` returns {id: mobject} — what is visible, where, lit or dimmed.
States are pure (they build fresh mobjects every call), so any beat can be drawn on its own.

- still     each beat's state, captured as a PNG (no animation)            → G2
- animatic  consecutive states joined by the default transition (480p)     → G3
- full      a beat's own `motion` where defined, the default otherwise     → G4 / final

Default transition between two states, by id:
  same id  → morph (Transform when the shapes are compatible, FadeTransform otherwise; silent swap if unchanged)
  new id   → fade in        missing id → fade out
  morph_from={"new_id": "old_id"} pairs pieces with different ids (e.g. a block becoming a word).
A custom motion(scene, prev, cur) plays whatever it wants; afterwards the engine makes `cur` exactly what is on screen.

Live beats (`Beat(name, play=fn)`, no state): `play(scene)` animates persistent actors kept on the film's Stage — the
way a film made before the engine (or one with time-dependent pieces) is written. The screen is whatever the code
leaves; stills fast-forward through the film and capture the frame at the end of each beat; animatic = full.
"""

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

import numpy as np
from manim import *
from PIL import Image

from ..kit.i18n import Translator, current_lang
from ..kit.primitives import label
from ..kit.scene import FW, StudioScene

MODES = ("still", "animatic", "full")


@dataclass
class Beat:
    name: str
    state: Callable | None = None           # state(stage) -> {id: mobject}; None for a live beat
    motion: Callable | None = None          # motion(scene, prev, cur), full mode only
    hold: float = 1.2                       # seconds on screen after the transition
    morph_from: dict = field(default_factory=dict)   # {new_id: old_id}
    note: str = ""                          # shown on the stills page
    run_time: float = 0.8                   # default transition duration
    play: Callable | None = None            # live beat: play(scene) on the persistent Stage


@dataclass
class Act:
    name: str                               # short id (studio act <film> <name>)
    title: str                              # chapter label, e.g. "01 · THE AI"
    toc: str                                # chapter name in the player
    beats: list
    auto_chapter: bool = True               # False: the act's beats call scene.chapter(...) themselves


def _signature(m):
    """Geometry + style of a mobject family, to detect 'unchanged' pieces."""
    out = []
    for f in m.family_members_with_points():
        out.append((f.points.round(4).tobytes(), str(f.get_stroke_color()), round(f.get_stroke_opacity(), 3),
                    round(f.get_stroke_width(), 3), str(f.get_fill_color()), round(f.get_fill_opacity(), 3)))
    return out


def _compatible(a, b):
    fa, fb = a.family_members_with_points(), b.family_members_with_points()
    return len(fa) == len(fb) and all(len(x.points) == len(y.points) for x, y in zip(fa, fb))


def transition_anims(prev: dict, cur: dict, morph_from=None, skip=()):
    """Default animations from state `prev` to state `cur` (ids in `skip` are left to the caller).
    Returns (anims, swaps): swaps are (old, new) pairs identical on screen, to exchange without animation."""
    morph_from = morph_from or {}
    anims, swaps, used = [], [], set()
    for k, new in cur.items():
        if k in skip:
            continue
        src = morph_from.get(k, k)
        old = prev.get(src) if src not in used else None   # a piece can only turn into one new piece
        if old is None:
            anims.append(FadeIn(new, scale=0.95))
            continue
        used.add(src)
        if src == k and _signature(old) == _signature(new):
            swaps.append((old, new))
        elif src == k and _compatible(old, new):
            anims.append(ReplacementTransform(old, new))
        else:
            anims.append(FadeTransform(old, new))
    for k, old in prev.items():
        if k not in used and k not in skip:
            anims.append(FadeOut(old, scale=0.95))
    return anims, swaps


class FilmScene(StudioScene):
    """Base of engine films. Subclasses set: title, acts (list of Act), FR (dict), and build_stage()."""
    title = "Film"
    acts: list = []
    FR: dict = {}

    def build_stage(self):
        """Shared data and factories used by the states (no mobjects kept between beats)."""
        return None

    # --- Entry point --------------------------------------------------------------------------------
    def construct(self):
        self.tr = Translator(self.FR)
        type(self).translate = staticmethod(self.tr)
        self.stage = self.build_stage()
        self.mode = os.environ.get("FILM_MODE", "full")
        if self.mode not in MODES:
            raise ValueError(f"FILM_MODE={self.mode} (expected {', '.join(MODES)})")
        if self.mode == "still":
            return self.stills()
        self.shown = {}
        self.run_acts([(a.name, [lambda a=a: self.play_act(a)]) for a in self.acts], self.title)

    # --- Animated modes -----------------------------------------------------------------------------
    def play_act(self, act):
        for i, beat in enumerate(act.beats):
            if beat.play is not None:  # live beat
                beat.play(self)
                if beat.hold > 0:
                    self.hold(beat.hold)
                continue
            cur = beat.state(self.stage)
            extra = self.chapter_anims(act) if i == 0 and act.auto_chapter else []
            if self.mode == "full" and beat.motion is not None:
                if extra:
                    self.play(*extra, run_time=0.7)
                beat.motion(self, self.shown, cur)
            else:
                anims, swaps = transition_anims(self.shown, cur, beat.morph_from)
                for old, new in swaps:
                    self.remove(old)
                    self.add(new)
                if anims or extra:
                    self.play(*anims, *extra, run_time=beat.run_time, rate_func=rate_functions.ease_in_out_cubic)
            self.settle(cur)
            self.hold(beat.hold)

    def settle(self, cur):
        """Make `cur` exactly what is on screen (plus the chapter label), in its order."""
        keep = {id(self.chapter_lbl)} if self.chapter_lbl is not None else set()
        self.remove(*[m for m in self.mobjects if id(m) not in keep])
        self.add(*cur.values())
        self.shown = cur

    def chapter_label(self, text):
        frame = self.camera.frame
        new = label(self.tr(text), 14, GREY_B, spacing=6).set_z_index(30)
        h0 = new.height

        def stick(m):
            s = frame.width / FW
            m.scale_to_fit_height(h0 * s)
            m.move_to(frame.get_corner(UL) + np.array([0.45, -0.4, 0]) * s, aligned_edge=UL)

        stick(new)
        new.add_updater(stick)
        return new

    def chapter_anims(self, act):
        """The act's chapter label replaces the previous one, during the act's first transition."""
        self.chapters.append([round(self.now(), 2), self.tr(act.toc)])
        new = self.chapter_label(act.title)
        anims = [FadeIn(new, shift=RIGHT * 0.15)]
        if self.chapter_lbl is not None:
            anims.insert(0, FadeOut(self.chapter_lbl, shift=LEFT * 0.1))
        self.chapter_lbl = new
        return anims

    # --- Still mode ---------------------------------------------------------------------------------
    def stills(self):
        live = any(b.play is not None for a in self.acts for b in a.beats)
        if live:  # fast-forward: every beat runs (skipped), the frame is captured at each beat's end
            self.chapters, self.chapter_lbl, self.shown = [], None, {}
            self.next_section("stills", skip_animations=True)
        out = Path(os.environ.get("FILM_OUT", "."))
        out.mkdir(parents=True, exist_ok=True)
        names = [a.name for a in self.acts]
        start, upto = os.environ.get("FILM_FROM"), os.environ.get("FILM_UPTO")
        lo = names.index(start) if start else 0
        hi = names.index(upto) if upto else len(names) - 1
        index, n = [], 0
        for ai, act in enumerate(self.acts):
            for bi, beat in enumerate(act.beats):
                n += 1
                if live:
                    if beat.play is not None:
                        beat.play(self)
                    if not lo <= ai <= hi:
                        if beat.hold > 0:
                            self.hold(beat.hold)
                        continue
                    self.renderer.update_frame(self, ignore_skipping=True)
                elif not lo <= ai <= hi:
                    continue
                else:
                    self.clear()
                    lbl = self.chapter_label(act.title)
                    lbl.clear_updaters()
                    self.add(*beat.state(self.stage).values(), lbl)
                    self.renderer.update_frame(self, ignore_skipping=True)
                fname = f"{n:02d}_{act.name}_{beat.name}.png"
                Image.fromarray(self.renderer.get_frame()).convert("RGB").save(out / fname)
                index.append({"n": n, "act": act.name, "act_title": self.tr(act.title), "beat": beat.name,
                              "note": beat.note, "motion": beat.motion is not None or beat.play is not None,
                              "hold": beat.hold, "file": fname})
                if live and beat.hold > 0:
                    self.hold(beat.hold)
        (out / "stills.json").write_text(json.dumps({"title": self.tr(self.title), "lang": current_lang(),
                                                     "beats": index}, ensure_ascii=False, indent=1))
