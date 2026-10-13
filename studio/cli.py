"""`studio` — render drafts, players, sheets, regressions and finals of the films in `films/`."""

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

from . import films
from .pipeline import player, regress, sheets
from .pipeline.render import manim, render


def _open(path: Path, args) -> None:
    print(path)
    if not getattr(args, "no_open", False) and sys.platform == "darwin":
        subprocess.run(["open", str(path)])


def _mode(args, film):
    mode = getattr(args, "mode", None) or "full"
    if mode != "full" and film.kind != "engine":
        raise SystemExit(f"{film.name} is a {film.kind} film: only engine films have an animatic mode")
    return mode


def _draft(args, film, tag, start=None, end=None, loop=True):
    """480p render + sheet + looping HTML player, then open the player."""
    mode = _mode(args, film)
    if mode != "full":
        tag = f"{mode}-{tag}"
    rd = render(film, f"{tag}-{args.lang}", "dev", args.lang, start, end, mode)
    sheets.grid(rd.video, rd.dir / "sheet.png")
    if rd.chapters:
        sheets.by_chapter(rd.video, rd.chapters, rd.dir / "chapters.png")
    page = player.build(rd.video, rd.chapters, rd.dir / "player.html", rd.meta.get("title", film.title), args.lang,
                        loop=loop)
    print(f"{rd.video}\n{rd.dir / 'sheet.png'}")
    _open(page, args)


def cmd_list(args):
    for name in films.names():
        f = films.load(name)
        print(f"{name}  [{f.kind}]  “{f.title}”  langs: {', '.join(f.langs)}\n    acts: {' '.join(f.acts)}")


def cmd_dev(args):
    _draft(args, films.load(args.film), "dev", loop=args.loop)


def cmd_act(args):
    f = films.load(args.film)
    _draft(args, f, f"act-{args.act}", f.check_act(args.act), args.act)


def cmd_range(args):
    f = films.load(args.film)
    if f.acts.index(f.check_act(args.start)) > f.acts.index(f.check_act(args.end)):
        raise SystemExit(f"'{args.start}' comes after '{args.end}' (acts: {' '.join(f.acts)})")
    _draft(args, f, f"range-{args.start}-{args.end}", args.start, args.end)


def _engine(film):
    if film.kind != "engine":
        raise SystemExit(f"{film.name} is a {film.kind} film: stills and animatics need an engine film (Film/Act/Beat)")
    return film


def cmd_still(args):
    from .pipeline.stills import stills
    f = _engine(films.load(args.film))
    d = stills(f, args.lang, args.act or args.start, args.act or args.end)
    print(d / "sheet.png")
    _open(d / "stills.html", args)


def cmd_animatic(args):
    f = _engine(films.load(args.film))
    args.mode = "animatic"
    if args.act:
        _draft(args, f, f"act-{f.check_act(args.act)}", args.act, args.act)
    else:
        _draft(args, f, "film", loop=True)


def cmd_new(args):
    """Start a new engine film from films/_template (brief.md, film.py, film.toml)."""
    import re as _re
    name = _re.sub(r"\W+", "_", args.name.lower()).strip("_")
    dest = films.FILMS / name
    if dest.exists():
        raise SystemExit(f"films/{name} already exists")
    shutil.copytree(films.FILMS / "_template", dest, ignore=shutil.ignore_patterns("__pycache__"))
    toml = dest / "film.toml"
    toml.write_text(toml.read_text().replace('"Film title"', json.dumps(args.title or args.name)))
    py = dest / "film.py"
    py.write_text(py.read_text().replace('title = "Film title"', f"title = {json.dumps(args.title or args.name)}"))
    for md in ("brief.md", "STATUS.md"):
        f = dest / md
        f.write_text(f.read_text().replace("<film title>", args.title or args.name).replace("<name>", name))
    print(f"films/{name}: brief.md · STATUS.md · film.py · film.toml — next (G1): studio extract {name} <source file>")


def cmd_extract(args):
    """G1: presentation / research doc → films/<film>/source.md (appends when called again)."""
    from .pipeline.extract import extract
    src = Path(args.source).expanduser().resolve()
    if not src.exists():
        raise SystemExit(f"No such file: {src}")
    out = extract(src, films.FILMS / args.film)
    print(f"{out} ({len(out.read_text(encoding='utf-8').splitlines())} lines)")


def cmd_final(args):
    if not args.validated:
        raise SystemExit("A final render needs the user's explicit validation of the 480p draft. "
                         "Re-run with --validated once it is validated.")
    f = films.load(args.film)
    rd = render(f, f"final-{args.lang}", "final", args.lang)
    title = rd.meta.get("title", f.title)
    slug = re.sub(r"\W+", "_", title).strip("_") + ("" if args.lang == "en" else f"_{args.lang}")
    mp4 = rd.dir / f"{slug}.mp4"
    shutil.move(rd.video, mp4)
    page = player.build(mp4, rd.chapters, rd.dir / f"{slug}.html", title, args.lang, dev=False)
    print(mp4)
    _open(page, args)


def cmd_sheet(args):
    video = Path(args.video)
    if args.chapters:
        chapters = json.loads(Path(args.chapters).read_text(encoding="utf-8"))
        out = Path(args.out) if args.out else video.with_name(video.stem + ".chapters.png")
        sheets.by_chapter(video, chapters, out, cols=args.cols or 3)
    else:
        out = Path(args.out) if args.out else video.with_name(video.stem + ".sheet.png")
        sheets.grid(video, out, n=args.n, cols=args.cols or 4)
    _open(out, args)


def cmd_frames(args):
    video = Path(args.video)
    if args.every:
        from .pipeline.video import info
        d = info(video)["duration"]
        times = [k * args.every for k in range(int(d // args.every) + 1)]
    else:
        times = args.at
    outdir = Path(args.out) if args.out else video.parent / "frames"
    for p in sheets.sample(video, times, outdir):
        print(p)


def cmd_player(args):
    video = Path(args.video)
    chapters = json.loads(Path(args.chapters).read_text(encoding="utf-8")) if args.chapters else [[0.0, args.title]]
    out = Path(args.out) if args.out else video.with_suffix(".html")
    _open(player.build(video, chapters, out, args.title, args.lang, dev=not args.final, loop=args.loop), args)


def cmd_baseline(args):
    f = films.load(args.film)
    for lang in args.lang or f.langs:
        if args.source:
            src = Path(args.source).resolve()
            video, chapters = regress.baseline_from_source(f, lang, src, args.scene_class)
            rev = subprocess.run(["git", "-C", str(src.parent), "describe", "--always", "--dirty"],
                                 capture_output=True, text=True).stdout.strip()
            source = f"{src}" + (f" @ {rev}" if rev else "")
        else:
            rd = render(f, f"baseline-{lang}", "dev", lang)
            video, chapters, source = rd.video, rd.chapters, f"{f.dir.name}/{f.scene_file}"
        print(regress.store(f, lang, video, chapters, source))


def cmd_regress(args):
    f = films.load(args.film)
    results = regress.regress(f, args.lang or f.langs)
    for r in results:
        print(f"{r.lang.upper()}: {'IDENTICAL' if r.ok else 'DIFFERENT'} — frames baseline {r.frames[0]} / "
              f"current {r.frames[1]}, identical {r.identical}, chapters {'equal' if r.chapters_equal else 'DIFFERENT'}")
        for a, b, d in r.ranges:
            print(f"    differs {a:.2f}–{b:.2f} s (max mean abs diff {d:.3f})")
    _open(f.out / "regress" / "index.html", args)
    sys.exit(0 if all(r.ok for r in results) else 1)


def cmd_gallery(args):
    """Render one still per kit piece into gallery/ (+ sheet.png, README.md)."""
    from PIL import Image
    gal = films.ROOT / "gallery"
    manim(gal, "scene.py", "Gallery", "gallery", "gallery", films.OUT / "gallery" / "media", {"GALLERY_OUT": str(gal)})
    index = json.loads((gal / "index.json").read_text())
    tiles = [(f"{cap}", Image.open(gal / f"{name}.png")) for name, cap, _ in index]
    sheets.sheet(tiles, gal / "sheet.png", cols=4, tile=(427, 240))
    rows = "\n".join(f"| {cap} | {desc} | ![{name}]({name}.png) |" for name, cap, desc in index)
    (gal / "README.md").write_text("# Kit gallery\n\nGenerated by `studio gallery` from `gallery/scene.py`: one still per "
                                   "primitive (p), actor (a) and motion (m: start · middle · end).\n\n"
                                   "![sheet](sheet.png)\n\n| Piece | What | Still |\n|---|---|---|\n" + rows + "\n")
    _open(gal / "sheet.png", args)


def main(argv=None):
    p = argparse.ArgumentParser(prog="studio", description=__doc__,
                                epilog="Outputs go to out/<film>/<tag>/. Rules and workflow: CLAUDE.md, "
                                       ".claude/skills/film/SKILL.md.")
    sub = p.add_subparsers(dest="cmd", required=True, metavar="<command>")

    def add(name, fn, help, film=True, lang=True, opens=True):
        s = sub.add_parser(name, help=help, description=help)
        if film:
            s.add_argument("film", help="film name (folder in films/)")
        if lang:
            s.add_argument("--lang", default="en", help="en (default) or fr")
        if opens:
            s.add_argument("--no-open", action="store_true", help="do not open the result")
        s.set_defaults(fn=fn)
        return s

    add("list", cmd_list, "list films and their acts", film=False, lang=False, opens=False)
    s = add("new", cmd_new, "start a new engine film from films/_template", film=False, lang=False, opens=False)
    s.add_argument("name", help="folder name (snake_case)")
    s.add_argument("--title", help="film title (default: the name)")
    s = add("extract", cmd_extract, "G1 · presentation or doc (.pptx .pdf .md) → films/<film>/source.md", lang=False,
            opens=False)
    s.add_argument("source", help="path to the .pptx / .pdf / .md")
    s = add("still", cmd_still, "G2 · every beat as a PNG (no animation) + sheet + HTML page (engine films)")
    s.add_argument("--act", help="only this act")
    s.add_argument("--from", dest="start", help="first act")
    s.add_argument("--to", dest="end", help="last act")
    s = add("animatic", cmd_animatic, "G3 · 480p with default transitions only + looping player (engine films)")
    s.add_argument("--act", help="only this act")
    s = add("dev", cmd_dev, "full film, 480p draft + HTML player")
    s.add_argument("--mode", choices=["full", "animatic"], help="engine films: full (default) or animatic")
    s.add_argument("--loop", action="store_true", help="player loops by default")
    s = add("act", cmd_act, "one act, 480p draft + looping HTML player")
    s.add_argument("--mode", choices=["full", "animatic"], help="engine films: full (default) or animatic")
    s.add_argument("act")
    s = add("range", cmd_range, "acts <from>..<to>, 480p draft + looping HTML player")
    s.add_argument("--mode", choices=["full", "animatic"], help="engine films: full (default) or animatic")
    s.add_argument("start", metavar="from")
    s.add_argument("end", metavar="to")
    s = add("final", cmd_final, "1080p60 render + mp4 + HTML — only after explicit validation")
    s.add_argument("--validated", action="store_true", help="confirm the user validated the draft")

    s = add("sheet", cmd_sheet, "contact sheet of a video (grid, or one frame per chapter)", film=False, lang=False)
    s.add_argument("video")
    s.add_argument("-n", type=int, default=12, help="frames in the grid (default 12)")
    s.add_argument("--cols", type=int, help="columns (default 4 for grid, 3 for chapters)")
    s.add_argument("--chapters", help="chapters.json → one frame at the middle of each chapter")
    s.add_argument("-o", "--out")
    s = add("frames", cmd_frames, "sample full-resolution frames as PNGs", film=False, lang=False, opens=False)
    s.add_argument("video")
    g = s.add_mutually_exclusive_group(required=True)
    g.add_argument("--at", type=float, nargs="+", metavar="T", help="times in seconds")
    g.add_argument("--every", type=float, metavar="S", help="one frame every S seconds")
    s.add_argument("-o", "--out", help="output folder (default: <video folder>/frames)")
    s = add("player", cmd_player, "build the HTML player for any video", film=False)
    s.add_argument("video")
    s.add_argument("--chapters", help="chapters.json ([[t, title], …])")
    s.add_argument("--title", default="Film")
    s.add_argument("--loop", action="store_true")
    s.add_argument("--final", action="store_true", help="no DEV tag in the title")
    s.add_argument("-o", "--out")

    add("gallery", cmd_gallery, "render one still per kit piece into gallery/ (PNGs, sheet, README)", film=False,
        lang=False)
    s = add("baseline", cmd_baseline, "store the regression baseline (intentional visual change only)",
            lang=False, opens=False)
    s.add_argument("--lang", action="append", help="language(s) (default: all of the film's)")
    s.add_argument("--source", help="render this scene file from an untouched temp copy instead of the film's own")
    s.add_argument("--scene-class", default="Film")
    s = add("regress", cmd_regress, "re-render and compare frame by frame with the baseline", lang=False)
    s.add_argument("--lang", action="append", help="language(s) (default: all of the film's)")

    args = p.parse_args(argv)
    args.fn(args)


if __name__ == "__main__":
    main()
