"""G2 stills: every beat's state as a PNG (no animation), a contact sheet and an HTML page grouped by act."""

import base64
import html as _html
import io
import json
import shutil

from PIL import Image

from ..films import Film
from . import sheets
from .render import manim


def stills(film: Film, lang: str = "en", start: str | None = None, end: str | None = None):
    tag = "stills" + (f"-{start}" + (f"-{end}" if end and end != start else "") if start else "") + f"-{lang}"
    d = film.out / tag
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    env = {"FILM_LANG": lang, "FILM_OUT": str(d), "FILM_MODE": "still"}
    if start:
        env["FILM_FROM"] = film.check_act(start)
        env["FILM_UPTO"] = film.check_act(end or start)
    manim(film.dir, film.scene_file, film.scene_class, "gallery", tag, film.out / "media", env)
    index = json.loads((d / "stills.json").read_text(encoding="utf-8"))
    beats = index["beats"]
    sheets.sheet([(f"{b['n']:02d} {b['act']} · {b['beat']}", Image.open(d / b["file"])) for b in beats],
                 d / "sheet.png", cols=4)
    page(index, d)
    return d


def _jpeg(path, width=960):
    img = Image.open(path).convert("RGB")
    img = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=88)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def page(index, d):
    groups, body = {}, []
    for b in index["beats"]:
        groups.setdefault((b["act"], b["act_title"]), []).append(b)
    for (act, title), beats in groups.items():
        body.append(f"<h2>{_html.escape(title)} <small>{act}</small></h2><div class='grid'>")
        for b in beats:
            tags = f"<span class='tag'>{'custom motion' if b['motion'] else 'default transition'}</span>" \
                   f"<span class='tag'>hold {b['hold']:g} s</span>"
            body.append(f"<figure><img src='{_jpeg(d / b['file'])}' alt=''><figcaption><b>{b['n']:02d} · "
                        f"{_html.escape(b['beat'])}</b>{tags}<br>{_html.escape(b['note'])}</figcaption></figure>")
        body.append("</div>")
    title = _html.escape(index["title"])
    (d / "stills.html").write_text(PAGE.replace("{{TITLE}}", title).replace("{{LANG}}", index["lang"])
                                   .replace("{{BODY}}", "\n".join(body)), encoding="utf-8")


PAGE = """<!doctype html>
<html lang="{{LANG}}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}} · stills</title>
<style>
  body { margin: 0; background: #000; color: #CFF8FF; font-family: "DIN Alternate", "Avenir Next", sans-serif; }
  main { max-width: 1400px; margin: 0 auto; padding: 24px 16px 48px; }
  h1, h2 { font-family: Futura, sans-serif; font-weight: normal; letter-spacing: .15em; text-transform: uppercase; }
  h1 { font-size: 24px; } h2 { font-size: 17px; margin: 36px 0 12px; } h2 small { color: #4f6b75; letter-spacing: .1em; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(min(420px, 100%), 1fr)); gap: 14px; }
  figure { margin: 0; } img { width: 100%; display: block; border: 1px solid #0f2a33; border-radius: 6px; }
  figcaption { font-size: 14px; color: #8fb3bd; padding: 6px 2px; line-height: 1.5; }
  figcaption b { color: #CFF8FF; letter-spacing: .08em; margin-right: 8px; }
  .tag { font-size: 11px; text-transform: uppercase; letter-spacing: .1em; color: #4f6b75; border: 1px solid #0f2a33;
         border-radius: 4px; padding: 1px 6px; margin-right: 6px; }
</style></head>
<body><main><h1>{{TITLE}} · stills</h1>
{{BODY}}
</main></body></html>
"""
