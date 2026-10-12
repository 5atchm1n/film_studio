"""StudioScene: the Manim scene every film derives from.

- Timing: animations shorter than MIN_RT are stretched (no abrupt pops); `slow` scales everything.
  Inside `with self.exact():` durations are taken as given (packets, typing, jolts).
- Acts: `run_acts([(name, [scene_fn, …]), …], title)` honours FILM_FROM / FILM_UPTO (earlier acts are computed
  but not drawn) and writes chapters.json + meta.json into FILM_OUT for the studio pipeline.
- Chapter label pinned top-left of the camera frame; an element can rise to become it (`chapter(src=…)`).
"""

import json
import os
from contextlib import contextmanager
from pathlib import Path

import numpy as np
from manim import *

from .i18n import current_lang
from .primitives import label

FW = config.frame_width


class StudioScene(MovingCameraScene):
    slow = 1.0        # slow-motion factor
    MIN_RT = 0.5      # minimum animation duration (avoids abrupt pops)
    _exact = False    # True inside `with self.exact()`

    @staticmethod
    def translate(text):
        """Overridden by films with a Translator (see kit.i18n)."""
        return text

    # --- Timing -----------------------------------------------------------------------------------------
    def play(self, *anims, **kw):
        rt = kw.get("run_time")
        if rt is None:
            rt = max([a.run_time for a in anims if isinstance(a, Animation)] or [1.0])
        if not self._exact and 0.1 < rt < self.MIN_RT:  # jolts (< 0.1 s) and exact blocks are exempt
            rt = self.MIN_RT
        kw["run_time"] = rt * self.slow
        super().play(*anims, **kw)

    @contextmanager
    def exact(self):
        """Durations inside this block are used as given (no MIN_RT stretch)."""
        self._exact = True
        try:
            yield
        finally:
            self._exact = False

    def wait(self, duration=1.0, *args, **kw):
        super().wait(duration * self.slow, *args, **kw)

    def hold(self, t=0.6):
        self.wait(t)

    def now(self):
        return float(self.renderer.time)

    # --- Acts -------------------------------------------------------------------------------------------
    def run_acts(self, acts, title):
        """acts = [(name, [scene_fn, …]), …]. Honours FILM_FROM / FILM_UPTO; writes chapters + meta to FILM_OUT."""
        self.chapters = []
        self.chapter_lbl = None
        names = [a[0] for a in acts]
        upto = os.environ.get("FILM_UPTO")  # FILM_UPTO=problem: stop after this act
        start = os.environ.get("FILM_FROM")  # FILM_FROM=problem: earlier acts are computed but not drawn
        for act in (upto, start):
            if act and act not in names:
                raise ValueError(f"Unknown act: {act} (acts: {', '.join(names)})")
        act_starts = {}
        for name, scenes in acts:
            act_starts[name] = round(self.now(), 2)
            if start:
                self.next_section(name, skip_animations=names.index(name) < names.index(start))
            for scene in scenes:
                scene()
            if upto == name:
                self.hold(0.8)
                break
        out = Path(os.environ.get("FILM_OUT", "."))
        out.mkdir(parents=True, exist_ok=True)
        (out / "chapters.json").write_text(json.dumps(self.chapters, ensure_ascii=False, indent=1))
        (out / "meta.json").write_text(json.dumps({"lang": current_lang(), "title": self.translate(title),
                                                   "acts": act_starts}, ensure_ascii=False))

    def chapter(self, text, toc=None, src=None, extra=()):
        """Small chapter label, pinned top-left of the camera frame. `src`: an element that rises to become it."""
        self.chapters.append([round(self.now(), 2), self.translate(toc or text)])
        frame = self.camera.frame
        new = label(self.translate(text), 14, GREY_B, spacing=6).set_z_index(30)
        h0 = new.height

        def stick(m):
            s = frame.width / FW
            m.scale_to_fit_height(h0 * s)
            m.move_to(frame.get_corner(UL) + np.array([0.45, -0.4, 0]) * s, aligned_edge=UL)

        stick(new)
        new.add_updater(stick)
        if src is not None:  # an element of the scene rises and becomes the chapter title
            self.play(FadeOut(self.chapter_lbl, shift=LEFT * 0.1), FadeTransform(src, new), *extra, run_time=0.8)
        elif self.chapter_lbl is None:
            self.play(FadeIn(new, shift=RIGHT * 0.15), run_time=0.5)
        else:  # the old title fades before the new one appears
            self.play(LaggedStart(FadeOut(self.chapter_lbl, shift=LEFT * 0.1), FadeIn(new, shift=RIGHT * 0.15),
                                  lag_ratio=0.7), run_time=0.7)
        self.chapter_lbl = new
