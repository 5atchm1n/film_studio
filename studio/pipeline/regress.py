"""Pixel regression: a stored baseline (frame hashes + mp4) and a frame-by-frame comparison.

Baseline files, per language, in `films/<film>/baseline/`:
  <lang>.json   fps, size, frame count, chapters, sha1 of every decoded RGB frame
  <lang>.mp4    the baseline render itself (to compute pixel differences when hashes differ)
  <lang>.png    contact sheet, one frame per chapter
"""

import base64
import datetime
import hashlib
import io
import json
import shutil
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image

from ..films import Film
from . import player, sheets
from .render import manim, render
from .video import frames, frames_at, info


def frame_hashes(video: Path) -> list[str]:
    return [hashlib.sha1(a.tobytes()).hexdigest()[:20] for _, a in frames(video)]


def store(film: Film, lang: str, video: Path, chapters: list, source: str) -> Path:
    b = film.baseline
    b.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(video, b / f"{lang}.mp4")
    data = {"film": film.name, "lang": lang, "source": source,
            "created": datetime.datetime.now().isoformat(timespec="seconds"), **info(video),
            "chapters": chapters, "hashes": frame_hashes(video)}
    data["frames"] = len(data["hashes"])
    (b / f"{lang}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    sheets.by_chapter(video, chapters, b / f"{lang}.png")
    return b / f"{lang}.json"


def baseline_from_source(film: Film, lang: str, source: Path, scene_class: str) -> tuple[Path, list]:
    """Render an untouched copy of another scene (e.g. the reference project) without writing next to it."""
    tmp = Path(tempfile.mkdtemp(prefix="studio-baseline-"))
    for f in source.parent.glob("*.py"):
        shutil.copyfile(f, tmp / f.name)
    video = manim(tmp, source.name, scene_class, "dev", f"baseline-{lang}", tmp / "media",
                  {"FILM_LANG": lang, "FILM_OUT": str(tmp)})
    chap = next(p for p in (tmp / "chapters.json", tmp / "film_chapters.json") if p.exists())
    out = film.out / f"baseline-{lang}"
    out.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(video, out / "video.mp4")
    chapters = json.loads(chap.read_text(encoding="utf-8"))
    shutil.rmtree(tmp)
    return out / "video.mp4", chapters


@dataclass
class Result:
    lang: str
    frames: tuple[int, int]            # baseline, current
    identical: int = 0
    ranges: list = field(default_factory=list)  # [(t_start, t_end, max mean-abs-diff)]
    worst: list = field(default_factory=list)   # [(t, diff, baseline img, current img)]
    chapters_equal: bool = True
    video: Path | None = None
    chapters: list = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.frames[0] == self.frames[1] == self.identical and self.chapters_equal


def compare(film: Film, lang: str, video: Path, chapters: list) -> Result:
    base = json.loads((film.baseline / f"{lang}.json").read_text(encoding="utf-8"))
    cur = frame_hashes(video)
    fps = base["fps"]
    r = Result(lang, (len(base["hashes"]), len(cur)), video=video, chapters=chapters)
    r.identical = sum(a == b for a, b in zip(base["hashes"], cur))
    r.chapters_equal = [[round(t, 2), s] for t, s in base["chapters"]] == [[round(t, 2), s] for t, s in chapters]
    bad = [k for k, (a, b) in enumerate(zip(base["hashes"], cur)) if a != b]
    if bad:  # pixel differences, from the stored baseline mp4
        diffs, worst = {}, []  # worst: the 3 largest differences, with their images
        keep = set(bad)
        for k, ((_, a), (_, b)) in enumerate(zip(frames(film.baseline / f"{lang}.mp4"), frames(video))):
            if k in keep:
                diffs[k] = float(np.abs(a.astype(np.int16) - b).mean())
                worst = sorted(worst + [(diffs[k], k, a, b)], key=lambda w: -w[0])[:3]
        start = prev = bad[0]
        for k in bad[1:] + [None]:
            if k is None or k != prev + 1:
                r.ranges.append((start / fps, prev / fps, max(diffs.get(i, 0.0) for i in range(start, prev + 1))))
                if k is not None:
                    start = k
            if k is not None:
                prev = k
        r.worst = [(k / fps, d, a, b) for d, k, a, b in sorted(worst, key=lambda w: w[1])]
    return r


def regress(film: Film, langs: list[str]) -> list[Result]:
    results = []
    for lang in langs:
        rd = render(film, f"regress-{lang}", "dev", lang)
        player.build(rd.video, rd.chapters, rd.dir / "player.html", rd.meta.get("title", film.title), lang, loop=True)
        results.append(compare(film, lang, rd.video, rd.chapters))
    report(film, results)
    return results


def _jpeg(img: Image.Image, width=640) -> str:
    img = img.convert("RGB")
    img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=85)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def report(film: Film, results: list[Result]) -> Path:
    """out/<film>/regress/index.html: summary + baseline vs current stills, one row per chapter."""
    rows = []
    for r in results:
        status = "IDENTICAL" if r.ok else "DIFFERENT"
        rows.append(f"<h2>{r.lang.upper()} · <span class='{status.lower()}'>{status}</span></h2>"
                    f"<p>frames: baseline {r.frames[0]} · current {r.frames[1]} · identical {r.identical} · "
                    f"chapters {'equal' if r.chapters_equal else 'DIFFERENT'} · "
                    f"<a href='../regress-{r.lang}/player.html'>loop page</a></p>")
        for a, b, d in r.ranges:
            rows.append(f"<p class='different'>differs {a:.2f}–{b:.2f} s · max mean abs diff {d:.3f}</p>")
        duration = info(r.video)["duration"]
        bounds = [t for t, _ in r.chapters] + [duration]
        mids = [(bounds[k] + bounds[k + 1]) / 2 for k in range(len(r.chapters))]
        base = frames_at(film.baseline / f"{r.lang}.mp4", mids)
        cur = frames_at(r.video, mids)
        rows.append("<div class='grid'><b>baseline</b><b>current</b>")
        for (t, a), (_, b), (_, title) in zip(base, cur, r.chapters):
            same = "same" if np.array_equal(a, b) else "diff"
            rows.append(f"<figure><img src='{_jpeg(Image.fromarray(a))}'><figcaption>{title} · {t:.1f} s</figcaption></figure>"
                        f"<figure class='{same}'><img src='{_jpeg(Image.fromarray(b))}'>"
                        f"<figcaption>{'pixel-identical' if same == 'same' else 'DIFFERENT'}</figcaption></figure>")
        for t, d, a, b in r.worst:
            delta = Image.fromarray(np.clip(np.abs(a.astype(np.int16) - b) * 4, 0, 255).astype(np.uint8))
            rows.append(f"<figure><img src='{_jpeg(Image.fromarray(a))}'><figcaption>worst {t:.2f} s</figcaption></figure>"
                        f"<figure class='diff'><img src='{_jpeg(delta)}'><figcaption>|diff| ×4 · {d:.3f}</figcaption></figure>")
        rows.append("</div>")
    out = film.out / "regress" / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(REPORT.replace("{{TITLE}}", f"Regression · {film.title}").replace("{{BODY}}", "\n".join(rows)),
                   encoding="utf-8")
    return out


REPORT = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}}</title>
<style>
  body { margin: 0; background: #000; color: #CFF8FF; font-family: "DIN Alternate", "Avenir Next", sans-serif; }
  main { max-width: 1320px; margin: 0 auto; padding: 24px 16px 48px; }
  h1, h2 { font-family: Futura, sans-serif; font-weight: normal; letter-spacing: .15em; text-transform: uppercase; }
  h1 { font-size: 24px; } h2 { font-size: 18px; margin-top: 36px; }
  p { color: #8fb3bd; } a { color: #00E5FF; }
  .identical, .same figcaption { color: #2BFF88; } .different, .diff figcaption { color: #FF3355; }
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
  .grid b { font-weight: normal; letter-spacing: .12em; text-transform: uppercase; color: #4f6b75; }
  figure { margin: 0; } img { width: 100%; display: block; border: 1px solid #0f2a33; }
  figcaption { font-size: 13px; padding: 4px 0; color: #8fb3bd; }
</style></head>
<body><main><h1>{{TITLE}}</h1>
{{BODY}}
</main></body></html>
"""
