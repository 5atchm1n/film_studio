"""Contact sheets and frame sampling (self-checks before showing a render)."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .video import frames_at, info

TILE = (427, 240)
GAP = 6


def _stamp(t: float) -> str:
    return f"{int(t // 60)}:{t % 60:04.1f}"


def _font(size=14):
    return ImageFont.load_default(size=size)


def sheet(tiles: list[tuple[str, Image.Image]], out: Path, cols: int = 4, tile=TILE) -> Path:
    """Grid of labelled tiles on black."""
    w, h = tile
    rows = (len(tiles) + cols - 1) // cols
    img = Image.new("RGB", (cols * (w + GAP) + GAP, rows * (h + GAP) + GAP), "#0b0f12")
    font = _font()
    for i, (caption, im) in enumerate(tiles):
        im = im.convert("RGB").resize(tile, Image.LANCZOS)
        d = ImageDraw.Draw(im)
        d.rectangle([0, h - 22, w, h], fill="#000000")
        d.text((8, h - 19), caption, fill="#CFF8FF", font=font)
        img.paste(im, (GAP + (i % cols) * (w + GAP), GAP + (i // cols) * (h + GAP)))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out)
    return out


def grid(video: Path, out: Path, n: int = 12, cols: int = 4) -> Path:
    """n frames evenly spaced over the video, timestamp on each tile."""
    duration = info(video)["duration"]
    picked = frames_at(video, [duration * (k + 0.5) / n for k in range(n)])
    return sheet([(_stamp(t), Image.fromarray(a)) for t, a in picked], out, cols)


def by_chapter(video: Path, chapters: list, out: Path, cols: int = 3) -> Path:
    """One frame at the midpoint of each chapter, captioned with its title."""
    duration = info(video)["duration"]
    bounds = [t for t, _ in chapters] + [duration]
    mids = [(bounds[k] + bounds[k + 1]) / 2 for k in range(len(chapters))]
    picked = frames_at(video, mids)
    return sheet([(f"{k + 1:02d} {title} · {_stamp(t)}", Image.fromarray(a))
                  for k, ((t, a), (_, title)) in enumerate(zip(picked, chapters))], out, cols)


def sample(video: Path, times: list[float], outdir: Path) -> list[Path]:
    """Full-resolution PNG of the frame at each time."""
    outdir.mkdir(parents=True, exist_ok=True)
    paths = []
    for t, a in frames_at(video, times):
        p = outdir / f"t{t:07.2f}.png"
        Image.fromarray(a).save(p)
        paths.append(p)
    return paths
