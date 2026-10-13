# Film Studio

Turns a presentation or research doc into a short concept video (Manim, minimal TRON look), through four
validated gates. The workflow lives in the `film` skill (`.claude/skills/film/SKILL.md`); this file holds the
rules and the commands.

## Working rules (validated by the user — always apply)
- Before each change or phase: ask ≤4 multiple-choice questions, recommended option first. Then build.
- Never render or announce a *final* without explicit validation. Iterate on 480p drafts + the HTML loop page.
- Commit before every change (each version must stay renderable). Never push unless asked.
- Self-check every render by sampling frames (`studio frames`, `studio sheet`) before showing it.
- Work one act at a time (`studio act`, `studio range`) for fast loops.
- `../visuels_mcp_harness/` is the read-only reference project: read it, never modify it.
- The reference film must stay pixel-identical: run `studio regress ai_retrieving_dynamic_data` after any change
  that could affect it (kit, engine, pipeline, its beats). Re-baseline only on an intentional visual change.

## Design defaults (see `.claude/skills/film/lessons.md` for the full list)
Minimal TRON (black, thin neon, DIN Alternate spaced caps, Futura numbers, Menlo code) · keywords, never sentences ·
morph transitions (elements pair up and transform) · dim until relevant · never stack semi-transparent copies ·
answers appear in the chat, the side explains the mechanism · explain once, then condense · end on words ·
no precise business figures unless provided.

## Commands
```bash
uv venv --python 3.12 .venv && uv pip install -e .   # setup (macOS fonts: DIN Alternate, Futura, Menlo)
studio list                                          # films and their acts
studio new <name> [--title T]                        # new engine film from films/_template (brief, film.py)
studio extract <film> <file.pptx|pdf|md>            # G1 · source doc → films/<film>/source.md
studio still <film> [--act A] [--lang fr]            # G2 · one PNG per beat + sheet + stills.html (seconds)
studio animatic <film> [--act A]                     # G3 · 480p, default transitions only
studio dev <film> [--lang fr] [--mode animatic]      # full film 480p + HTML player (engine: custom motions)
studio act <film> <act>                              # one act 480p + loop page
studio range <film> <from> <to>                      # acts from..to 480p + loop page
studio sheet <video> [-n 8] [--chapters out.json]    # contact sheet (grid, or one frame per chapter)
studio frames <video> --at 12.5 40 | --every 5       # sample frames as PNGs (self-checks)
studio player <video> --chapters chapters.json       # rebuild the HTML player for any render
studio regress <film>                                # re-render EN + FR, compare to baseline frame by frame
studio gallery                                       # one still per kit piece → gallery/ (commit the PNGs)
studio baseline <film> [--source scene.py]           # store a new baseline (intentional change only)
studio final <film> --validated                      # 1080p60 + mp4 + HTML — only after explicit validation
```
`.venv/bin/studio` works without activating the venv. Outputs go to `out/<film>/<tag>/` (never the source folder).

## Layout
```
studio/            python package: cli.py, films.py (manifests), pipeline/ (render, player, sheets, regress, video)
studio/engine/     Film / Act / Beat, modes still · animatic · full (FILM_MODE)
studio/kit/        primitives → actors → motions; layout (named anchors); i18n (EN source, FR dict); scene (StudioScene)
gallery/           scene.py + one committed PNG per kit piece (README.md shows them all)
films/<name>/      film.toml (manifest) + film.py · brief.md · source.md · STATUS.md (gate, decisions, next step);
                   baseline/ = regression reference (the reference film)
films/_template/   starting point for a new film (brief.md, STATUS.md, film.py, film.toml) — use `studio new`
.claude/skills/film/  the gated workflow: SKILL.md (loop) + g1_brief … g4_polish.md, lessons.md, checklist.md
docs/              history: process log, versions + frames, audit, plan, blog backbone (README.md)
out/               renders (gitignored)
```

## Kit rules
- A film derives from `kit.scene.StudioScene` (timing, `with self.exact()`, `run_acts`, `chapter`).
- On-screen text is written in English; the film's `FR` dict + `kit.i18n.Translator` give French. Actors take
  already-translated text.
- Act hand-offs live in one `@dataclass(slots=True) Stage` (`self.st`): no attribute is created inside an act.
- Never assign `self.color` (or other style names) on a VGroup subclass: Manim treats it as a setter.
- Highlights recolour in place (`motions.highlight`); the reference film keeps its lit copies (pixel-identical).
- Every new kit piece gets a function in `gallery/scene.py`; re-run `studio gallery` and look at the sheet.

## Film manifest (`films/<name>/film.toml`)
`kind = "legacy"` (none left; still supported) = a plain Manim scene driven by environment variables:
`FILM_LANG` (en|fr), `FILM_FROM` / `FILM_UPTO` (act names: earlier acts are computed but not drawn),
`FILM_OUT` (directory where the scene writes `chapters.json` = `[[t, title], …]` and
`meta.json` = `{lang, title, acts: {name: start_t}}`).

`kind = "engine"` films derive from `studio.engine.FilmScene`: `acts = [Act(name, title, toc, [Beat(...)])]`, `FR`,
`build_stage()`. A `Beat(name, state, motion=None, hold, morph_from, note, run_time)`:
- `state(stage) -> {id: mobject}` is **pure** (fresh mobjects each call): any beat can be drawn alone (stills).
- Default transition by id: same id → morph (silent swap if unchanged), new → fade in, missing → fade out;
  `morph_from={"new": "old"}` pairs different ids (block → word).
- `motion(scene, prev, cur)` (full mode only) plays anything; the engine then puts exactly `cur` on screen.
- Act chapter labels are automatic (`auto_chapter=False`: the beats call `scene.chapter` themselves).
- Live beats `Beat(name, play=fn, hold)`: `play(scene)` animates persistent actors on the Stage (time-dependent
  pieces, films ported from plain scenes). Stills fast-forward and capture each beat's end; animatic = full.
  Example: `films/ai_retrieving_dynamic_data` (35 live beats, pixel-identical to its pre-engine baseline).

## Roadmap
Plan: `docs/PLAN_FILM_STUDIO.md` (phases 0–7). Done: 0 bootstrap · 1 tooling · 2 legacy migration · 3 kit extraction · 4 engine · 5 skill gates · 6 docs.
Next: 7 pilot film.
