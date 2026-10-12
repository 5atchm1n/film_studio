"""Self-contained HTML player: embedded video, chapters, time scrubber, frame stepping, loop."""

import base64
import html as _html
from pathlib import Path

from .video import info

UI = {
    "en": {"pause": "Pause", "play": "Play", "restart": "Restart", "loop_label": "Loop", "fs": "Full screen",
           "hint": "Space: play / pause · ← →: chapter · , .: frame by frame"},
    "fr": {"pause": "Pause", "play": "Lecture", "restart": "Recommencer", "loop_label": "En boucle", "fs": "Plein écran",
           "hint": "Espace : lecture / pause · ← → : chapitre · , . : image par image"},
}


def build(video: Path, chapters: list, out: Path, title: str, lang: str = "en", dev: bool = True,
          loop: bool = False) -> Path:
    ui = UI.get(lang, UI["en"])
    fps = info(video)["fps"]
    items = "\n".join(
        f'<li data-t="{t:.2f}"><span class="n">{k + 1:02d}</span><span>{_html.escape(name)}</span>'
        f'<span class="time">{int(t // 60)}:{int(t % 60):02d}</span></li>'
        for k, (t, name) in enumerate(chapters))
    page = (TEMPLATE.replace("{{LANG}}", lang).replace("{{TITLE}}", _html.escape(title))
            .replace("{{H1}}", _html.escape(title) + (" · DEV" if dev else ""))
            .replace("{{ITEMS}}", items).replace("{{FPS}}", f"{fps:g}")
            .replace("{{LOOP}}", " checked" if loop else "").replace("{{LOOPJS}}", "true" if loop else "false"))
    for key, text in ui.items():
        page = page.replace("{{%s}}" % key.upper(), text)
    page = page.replace("{{VIDEO}}", base64.b64encode(video.read_bytes()).decode())
    out.write_text(page, encoding="utf-8")
    return out


TEMPLATE = """<!doctype html>
<html lang="{{LANG}}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}}</title>
<style>
  :root { --bg: #000; --fg: #CFF8FF; --dim: #4f6b75; --sens: #00E5FF; --cadre: #FF9E1B; --line: #0f2a33; }
  * { box-sizing: border-box; }
  body { margin: 0; background: var(--bg); color: var(--fg); font-family: "DIN Alternate", "Avenir Next", Futura, sans-serif; }
  main { max-width: 1200px; margin: 0 auto; padding: 32px 16px 48px; }
  header { margin-bottom: 20px; }
  h1 { font-family: Futura, "DIN Alternate", sans-serif; font-weight: normal; text-transform: uppercase;
       letter-spacing: .25em; font-size: clamp(20px, 3vw, 32px); margin: 0; }
  .player { position: relative; border: 1px solid var(--line); border-radius: 10px; overflow: hidden; background: #000;
            box-shadow: 0 0 40px rgba(0, 229, 255, .08); }
  video { display: block; width: 100%; height: auto; }
  .scrub { display: flex; align-items: center; gap: 12px; margin-top: 12px; }
  .scrub input { flex: 1; accent-color: var(--sens); cursor: pointer; }
  .scrub output { font-size: 14px; color: var(--dim); font-variant-numeric: tabular-nums; min-width: 150px; text-align: right; }
  .controls { display: flex; gap: 10px; margin: 14px 0 22px; align-items: center; flex-wrap: wrap; }
  button { font: inherit; color: var(--fg); background: transparent; border: 1px solid var(--line); border-radius: 6px;
           padding: 6px 14px; cursor: pointer; }
  button, li { text-transform: uppercase; letter-spacing: .12em; font-size: 13px; }
  button:hover { border-color: var(--dim); }
  .hint { color: var(--dim); font-size: 14px; margin-left: auto; }
  ol { list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 6px; }
  li { display: flex; gap: 12px; align-items: baseline; padding: 10px 12px; border-radius: 6px; cursor: pointer;
       border: 1px solid transparent; color: var(--dim); transition: color .2s, border-color .2s; }
  li:hover { color: var(--fg); }
  li.on { color: var(--fg); border-color: var(--line); background: #031014; }
  li .n { font-variant-numeric: tabular-nums; color: var(--sens); }
  li.on .n { color: var(--cadre); }
  li .time { margin-left: auto; font-size: 13px; font-variant-numeric: tabular-nums; }
</style>
</head>
<body>
<main>
  <header><h1>{{H1}}</h1></header>
  <div class="player">
    <video id="v" autoplay muted playsinline preload="auto" src="data:video/mp4;base64,{{VIDEO}}"></video>
  </div>
  <div class="scrub"><input type="range" id="t" min="0" max="1" step="0.001" value="0"><output id="tt">0.0 s</output></div>
  <div class="controls">
    <button id="play">{{PAUSE}}</button>
    <button id="restart">{{RESTART}}</button>
    <label><input type="checkbox" id="loop"{{LOOP}}> {{LOOP_LABEL}}</label>
    <button id="fs">{{FS}}</button>
    <span class="hint">{{HINT}}</span>
  </div>
  <ol id="ch">
{{ITEMS}}
  </ol>
</main>
<script>
  const FPS = {{FPS}};
  const v = document.getElementById('v'), t = document.getElementById('t'), tt = document.getElementById('tt'),
        play = document.getElementById('play');
  v.loop = {{LOOPJS}};
  let dragging = false;
  const show = () => { tt.textContent = v.currentTime.toFixed(2) + ' / ' + (v.duration || 0).toFixed(1) + ' s · #'
                       + Math.round(v.currentTime * FPS); };
  v.addEventListener('loadedmetadata', () => { t.max = v.duration; show(); });
  t.addEventListener('input', () => { dragging = true; v.pause(); v.currentTime = +t.value; show(); });
  t.addEventListener('change', () => { dragging = false; });
  const items = [...document.querySelectorAll('#ch li')], starts = items.map(li => +li.dataset.t);
  const current = () => { let i = 0; starts.forEach((s, k) => { if (v.currentTime + 0.05 >= s) i = k; }); return i; };
  const seek = i => { v.currentTime = starts[Math.max(0, Math.min(i, starts.length - 1))] + 0.01; v.play(); };
  v.addEventListener('timeupdate', () => {
    if (!dragging) t.value = v.currentTime;
    show();
    const c = current(); items.forEach((li, k) => li.classList.toggle('on', k === c));
  });
  v.addEventListener('seeked', show);
  v.addEventListener('play', () => play.textContent = '{{PAUSE}}');
  v.addEventListener('pause', () => play.textContent = '{{PLAY}}');
  play.onclick = () => v.paused ? v.play() : v.pause();
  document.getElementById('restart').onclick = () => seek(0);
  document.getElementById('loop').onchange = e => v.loop = e.target.checked;
  document.getElementById('fs').onclick = () => (v.requestFullscreen || v.webkitEnterFullscreen).call(v);
  items.forEach((li, k) => li.onclick = () => seek(k));
  document.addEventListener('keydown', e => {
    if (e.target === t && e.key.startsWith('Arrow')) return;
    if (e.code === 'Space') { e.preventDefault(); play.click(); }
    if (e.key === ',' || e.key === '.') { v.pause(); v.currentTime = Math.max(0, v.currentTime + (e.key === '.' ? 1 : -1) / FPS); }
    if (e.key === 'ArrowRight') seek(current() + 1);
    if (e.key === 'ArrowLeft') seek(v.currentTime - starts[current()] > 1.5 ? current() : current() - 1);
  });
</script>
</body>
</html>
"""
