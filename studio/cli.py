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
from .pipeline.render import render


def _open(path: Path, args) -> None:
    print(path)
    if not getattr(args, "no_open", False) and sys.platform == "darwin":
        subprocess.run(["open", str(path)])


def _draft(args, film, tag, start=None, end=None, loop=True):
    """480p render + sheet + looping HTML player, then open the player."""
    rd = render(film, f"{tag}-{args.lang}", "dev", args.lang, start, end)
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
    s = add("dev", cmd_dev, "full film, 480p draft + HTML player")
    s.add_argument("--loop", action="store_true", help="player loops by default")
    s = add("act", cmd_act, "one act, 480p draft + looping HTML player")
    s.add_argument("act")
    s = add("range", cmd_range, "acts <from>..<to>, 480p draft + looping HTML player")
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
