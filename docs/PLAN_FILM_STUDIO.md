# Plan — Film Studio: from a brief to a concept video

> Copied from `visuels_mcp_harness/docs/` (@ 6fb3c32, 13 Oct 2026) into film_studio (Phase 6). Paths such as `_archives/…`, `../film.py` or `../ETAT_PROJET.md` refer to `../visuels_mcp_harness/` (read-only reference; `ETAT_PROJET.md` is also in `history/`).

*Written 13 Oct 2026, after making "AI - Retrieving dynamic data" (≈130 requests, ~50 versions over 3 days).*
*Goal: never rebuild a film from scratch again. Start from a presentation or research, get a few acts, see stills in
seconds, add motion only where it carries the concept, render the full video at any time.*

**Status (Phase 6, 13 Oct 2026):** phases 0–6 done in `film_studio/` — see `VERSIONS.md` § Generation 5.
Deviations from this plan, decided with the user: docs copied, not moved (the reference stays read-only); act names
and on-screen source text in English (FR dict); the skill has one file per gate + `STATUS.md` per film;
`studio extract` added for G1; the beats pilot lives in its own film folder. Next: Phase 7 (pilot film).

---

## 1. What we learned (the history this plan is built on)

Sources: `docs/PROCESS_LOG.md` (every request), `docs/VERSIONS.md` + `docs/frames/INDEX.md` (49 versions with frames),
`docs/AUDIT.md` (code audit), `ETAT_PROJET.md`, git log of `visuels_mcp_harness`.

### 1.1 How the film actually got made
1. Idea + constraint (MCP = semantic layer, Harness = trust) → speech first → Manim slides (gen 1).
2. Slides rejected: "one story, one flow, one style"; chef metaphor "too childish" → TRON minimal, AI = chip (gen 2).
3. Standalone film with acts, no speaker (gen 3, v6–v8). Bottleneck = full renders → per-act drafts, contact sheets,
   looping dev pages with a time scrubber.
4. Story rework (gen 4, ~30 snapshots in one evening): problem → semantic layer → harness → together,
   each change validated on a 480p loop page, snapshot saved before each change.
5. Clean-up: dead code removed, acts renamed, `film_kit.py` extracted — verified pixel-identical each step.

### 1.2 Design rules the user validated (must become defaults)
- Minimal TRON look: black, neon thin strokes, DIN Alternate labels in spaced capitals, Futura numbers, Menlo code.
- No full sentences on screen; keywords only. No childish metaphors. Academic, not glitchy (no glitch effects).
- One continuous story with morph transitions: elements pair up and transform (FadeTransform per element), not cuts.
- A recurring "actor" set: chat window (the user, with an identity badge), AI chip, circuit rails, data blocks.
- Answers appear in the chat; the side of the screen explains the mechanism (panels).
- Dim everything that is not relevant yet; light it only when used. Never stack semi-transparent copies.
- Right-angle circuits; packets travel along rails; one path lit per call.
- Explain in detail once, then condense into icons / big-picture blocks.
- Chapter label top-left; a question/finding can rise to become the chapter title.
- No precise business figures unless provided (orders of magnitude only).
- End on words that summarise the concepts (blocks morph into words), never on a black screen.

### 1.3 Workflow rules the user validated
- Ask multiple-choice questions before each change (≤4, recommended option first).
- Never render or announce a "final" without explicit validation; iterate on 480p + HTML loop page.
- Snapshot/commit before every change; keep every version renderable.
- Self-check every render with sampled frames before showing it.
- Short, fast loops: one act at a time (`dev4`, `dev5`, `dev35`), scrubber + frame stepping in the page.

### 1.4 Technical pain points (from AUDIT.md)
- One 1,700-line scene; acts hand objects to each other through ~40 implicit attributes → removing something in act 4 breaks act 5.
- Shapes mutated mid-film; z-index and opacity managed by hand; highlight = overlay copies.
- Pipeline duplicated per preview (`dev4`, `dev5`, `dev35`…); outputs written in the source folder.
- Everything is a full animation: there is no way to see a frame without animating up to it.

---

## 2. Target: what the code must reflect

```
brief (md)  ──G1──▶  acts & beats  ──G2──▶  stills (PNG sheet)  ──G3──▶  animatic (480p, default transitions)
                                                                      ──G4──▶  polish (custom motion) + final 1080p + HTML
```
- **A film = acts → beats.** A beat is a *state* of the screen (which actors, where, what text, what is lit) plus an
  optional custom *motion* to reach it.
- **Same film code, three render modes**
  - `still`: build each beat's state and snapshot it (no animation) → contact sheet in seconds.
  - `animatic`: go from state to state with a default transition (paired morph / fade) → 480p video.
  - `full`: use the beat's custom motion when defined, the default transition otherwise → dev 480p or final 1080p.
- **The kit grows slowly**: primitives (colours, neon, rails, icons, chip) → actors/widgets (chat, badge, panel,
  band, data block, code file, harness frame) → motions (morph pairs, send packet, flash along, dim/light,
  condense, rise-to-title, words-from-blocks). Each new piece gets a gallery still.
- **The current film keeps rendering at all times** (regression baseline = pixel diff against a stored render).
- **Workflow lives in the repo** as a Claude Code skill (`.claude/skills/film/`), so cloning the repo brings it along.

The exact storyboard format is deliberately left open: start with plain Python (beats as functions returning
state), iterate toward a declarative description only where it clearly saves time.

---

## 3. Phases

### Phase 0 — Bootstrap the new repo `film_studio/` (sibling of `visuels_mcp_harness/`)
- Structure (proposal):
  ```
  film_studio/
    CLAUDE.md                     # project rules (from §1.2–1.3), commands, layout
    .claude/skills/film/SKILL.md  # the workflow skill (gates G1–G4)
    .claude/skills/film/…         # templates: brief.md, acts.md, checklist, lessons
    studio/                       # python package
      kit/  (primitives.py, actors.py, motions.py, layout.py, i18n.py)
      engine/ (film.py: Film/Act/Beat, modes still|animatic|full)
      pipeline/ (cli.py, player_html.py, sheets.py, regress.py)
    films/
      ai_retrieving_dynamic_data/ (legacy scene, migrated as-is + baseline)
      _template/ (brief.md, film.py skeleton)
    gallery/                      # one still per kit piece
    docs/                         # history + blog (moved from visuels_mcp_harness/docs)
    requirements.txt, .gitignore (media/, *.mp4, *.html, out/)
  ```
- Git repo, venv (Manim CE 0.21 pinned, PyAV, Pillow, numpy). No ffmpeg dependency (PyAV for frames).
- Keep `visuels_mcp_harness/` untouched as the reference.

### Phase 1 — Port the tooling (nothing lost)
- One CLI replaces `dev.sh` branches: `studio still|animatic|dev|range <from> <to>|act <name>|final <film>`.
- HTML player (from `build_auto_html.py`): chapters, scrubber, frame stepping, loop, partial-range chapter offsets.
- Contact sheets (`planche.py` + the frames agent script), frame sampling for self-checks.
- `regress`: store a baseline render, compare frame-by-frame (mean abs diff), report differing ranges.
- Outputs go to `out/<film>/` (never the source folder); chapters/meta JSON there too.

### Phase 2 — Migrate the current film as the first citizen
- `films/ai_retrieving_dynamic_data/legacy_scene.py` = today's `film.py` + `film_kit.py`, unchanged behaviour.
- Store baseline; `studio regress ai_retrieving_dynamic_data` must pass (pixel-identical) → proves tooling parity.

### Phase 3 — Extract the kit from the legacy film (still pixel-identical)
- Move primitives (done in `film_kit.py`) → `kit/primitives.py`.
- Actors: chat (+bubbles, replies, badge), chip, band/MCP, data block, panel frame, tools strip, code file, harness frame.
- Motions: `morph` (paired FadeTransform), `send` (packet along rail), `flash_along`, `dim/light` (opacity-safe),
  `highlight(path)` (recolour in place, returns restore), `rise_to_title`, `condense`, `words_from_blocks`.
- Layout grid: named anchors (left chat, centre chip, right panel, band, data) instead of magic numbers.
- Explicit state: one `Stage` object holding the actors; no attribute invented inside an act.
- After each extraction: `regress` passes.

### Phase 4 — Engine: Film / Act / Beat with three modes
- `Beat(state=fn, motion=fn|None, hold=s, title=…)`; `Act(name, beats)`; `Film(acts, lang)`.
- `still` mode: apply states with `self.add/remove` only, snapshot each beat → `out/<film>/stills.png` + per-beat PNGs.
- `animatic` mode: default transition between consecutive states = paired morph of actors with the same id,
  fade in/out for the rest.
- `full` mode: custom motion if defined.
- Chapters + i18n (EN default, FR switch) built in.
- Re-express 1–2 acts of the legacy film as beats to validate the model (compare against legacy frames by eye).

### Phase 5 — The skill / workflow (gates)
- **G1 Brief**: input = a presentation or research doc (md/pdf/pptx export) → `films/<name>/brief.md`
  (audience, the one idea, 3–6 acts, one key image per act, vocabulary, actors). MCQ questions to settle.
- **G2 Stills**: write states only → `studio still` → sheet of one frame per beat. Iterate on layout/text here.
- **G3 Animatic**: `studio animatic` → 480p loop page with default transitions. Validate pacing and story.
- **G4 Polish & final**: add custom motions only where the concept needs it; per-act loop pages; then
  `studio final` (1080p + HTML) only after explicit validation.
- Every gate: ask MCQ first, snapshot/commit before changes, self-check frames, never skip validation.
- `lessons.md` in the skill: the design rules of §1.2 (kept up to date as new feedback arrives).

### Phase 6 — Docs & blog
- Move `docs/` (process log, versions, frames, audit, blog backbone) into `film_studio/docs/`.
- Add the post-migration baseline to `VERSIONS.md`; fill `BLOG_BACKBONE.md` sections later.

### Phase 7 — Pilot
- Make a second short film (≤60 s) from a new brief using only G1–G4. Measure: requests needed, time to first
  stills, time to animatic. Feed gaps back into the kit.

---

## 4. Definition of done
- Cloning `film_studio` + `pip install -r requirements.txt` gives: the skill, the CLI, the legacy film rendering
  pixel-identical, a template film, the gallery.
- A new film reaches a stills sheet from a brief in one session without writing animation code.
- The legacy film and any new film can be rendered (dev or final) at any time.

## 5. Risks
- Over-designing the declarative format → keep Python-first, extract patterns only after they repeat twice.
- Manim upgrade drift → keep 0.21 pinned until regression tooling is solid.
- Fonts (DIN Alternate, Futura, Menlo) are macOS fonts → document; fallbacks for other machines.
