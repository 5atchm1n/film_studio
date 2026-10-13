"""Render a film (or a range of its acts) with Manim into `out/<film>/<tag>/`.

Legacy films are Manim scenes driven by environment variables (see CLAUDE.md, "Film manifest"):
FILM_LANG, FILM_FROM, FILM_UPTO, FILM_OUT. The scene writes chapters.json + meta.json into FILM_OUT.
"""

import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from ..films import Film

QUALITY = {"dev": ("-ql", "480p15"), "final": ("-qh", "1080p60"), "gallery": ("-qm", "720p30")}


@dataclass
class Render:
    dir: Path
    video: Path
    chapters: list  # [[t, title], …], relative to the start of `video`
    meta: dict


def manim(scene_dir: Path, scene_file: str, scene_class: str, quality: str, name: str, media_dir: Path,
          env: dict) -> Path:
    """Run Manim in `scene_dir`; return the rendered mp4 path."""
    flag, folder = QUALITY[quality]
    cmd = [sys.executable, "-m", "manim", "render", flag, "--disable_caching", "--media_dir", str(media_dir),
           "-o", name, scene_file, scene_class]
    full_env = {**os.environ, "PYTHONWARNINGS": "ignore", "PYTHONPATH": str(scene_dir), **env}
    subprocess.run(cmd, cwd=scene_dir, env=full_env, check=True)
    return media_dir / "videos" / Path(scene_file).stem / folder / f"{name}.mp4"


def render(film: Film, tag: str, quality: str = "dev", lang: str = "en", start: str | None = None,
           end: str | None = None, mode: str = "full") -> Render:
    """mode (engine films only): animatic = default transitions everywhere; full = custom motions where defined."""
    if lang not in film.langs:
        raise SystemExit(f"{film.name} has no '{lang}' version (langs: {', '.join(film.langs)})")
    d = film.out / tag
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    env = {"FILM_LANG": lang, "FILM_OUT": str(d), "FILM_MODE": mode}
    if start:
        env["FILM_FROM"] = film.check_act(start)
    if end:
        env["FILM_UPTO"] = film.check_act(end)
    rendered = manim(film.dir, film.scene_file, film.scene_class, quality, tag, film.out / "media", env)
    video = d / "video.mp4"
    shutil.move(rendered, video)
    chapters = json.loads((d / "chapters.json").read_text(encoding="utf-8"))
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
    if start:  # earlier acts were computed but not drawn: shift chapter times onto the partial video
        t0 = meta["acts"][start]
        chapters = [[round(t - t0, 2), title] for t, title in chapters if t >= t0 - 1e-6]
    (d / "chapters.json").write_text(json.dumps(chapters, ensure_ascii=False, indent=1), encoding="utf-8")
    return Render(d, video, chapters, meta)
